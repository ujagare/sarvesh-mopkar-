const TO_EMAIL = process.env.CONTACT_TO_EMAIL || "coach@sarveshmopkar.co";
const FROM_EMAIL =
  process.env.RESEND_FROM_EMAIL || "Sarvesh Mopkar Website <onboarding@resend.dev>";
const ALLOWED_ORIGIN = process.env.ALLOWED_ORIGIN || "";
function cleanEnv(value = "") {
  return String(value).trim().replace(/^['"]|['"]$/g, "");
}

function normalizeSupabaseUrl(value = "") {
  const cleaned = cleanEnv(value);
  if (!cleaned) return "";
  if (/^https?:\/\//i.test(cleaned)) return cleaned;
  if (/^[a-z0-9]{20}$/i.test(cleaned)) {
    return `https://${cleaned}.supabase.co`;
  }
  return cleaned;
}

function isSupabaseUrl(value = "") {
  return /^https:\/\/[a-z0-9]+\.supabase\.co$/i.test(normalizeSupabaseUrl(value).replace(/\/+$/, ""));
}

function isSupabaseKey(value = "") {
  const cleaned = cleanEnv(value);
  return /^sb_(?:secret|publishable)_[A-Za-z0-9._-]+$/.test(cleaned) || /^eyJ[A-Za-z0-9._-]+$/.test(cleaned);
}

function firstMatching(values, predicate) {
  return values.map(cleanEnv).find((value) => value && predicate(value)) || "";
}

function getSupabaseConfig() {
  const urlCandidates = [
    process.env.SUPABASE_URL,
    process.env.NEXT_PUBLIC_SUPABASE_URL,
    process.env.VITE_SUPABASE_URL,
    process.env.SUPABASE_PROJECT_URL,
    process.env.SUPABASE_PROJECT_REF,
    "https://yhspeotjjjkeryodqxtn.supabase.co",
  ];
  const keyCandidates = [
    process.env.SUPABASE_SERVICE_ROLE_KEY,
    process.env.SUPABASE_SERVICE_KEY,
    process.env.SUPABASE_SECRET_KEY,
    process.env.SUPABASE_ANON_KEY,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    process.env.VITE_SUPABASE_ANON_KEY,
    process.env.SUPABASE_URL,
  ];

  const url = firstMatching(urlCandidates, isSupabaseUrl);
  const key = firstMatching(keyCandidates, isSupabaseKey);
  return {
    key,
    url: normalizeSupabaseUrl(url).replace(/\/+$/, ""),
  };
}

function getPublicErrorMessage(error) {
  const message = String(error?.message || "Supabase insert failed.");
  return message
    .replace(/Bearer\s+[A-Za-z0-9._-]+/gi, "Bearer [redacted]")
    .replace(/sb_(?:secret|publishable)_[A-Za-z0-9._-]+/gi, "sb_[redacted]")
    .replace(/eyJ[A-Za-z0-9._-]+/g, "eyJ[redacted]")
    .replace(/apikey['"]?\s*:\s*['"][^'"]+['"]/gi, "apikey: [redacted]")
    .slice(0, 500);
}

const SUPABASE_CONTACT_TABLE = cleanEnv(process.env.SUPABASE_CONTACT_TABLE) || "contacts";
const RATE_LIMIT_WINDOW_MS = 60 * 1000;
const RATE_LIMIT_MAX = 3;
const rateLimitStore = new Map();

function sendJson(res, statusCode, body) {
  res.statusCode = statusCode;
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  res.end(JSON.stringify(body));
}

function escapeHtml(value = "") {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function cleanText(value = "", maxLength = 1000) {
  return String(value).trim().slice(0, maxLength);
}

function getClientIp(req) {
  const forwardedFor = req.headers["x-forwarded-for"];
  if (typeof forwardedFor === "string" && forwardedFor.trim()) {
    return forwardedFor.split(",")[0].trim();
  }

  return req.socket?.remoteAddress || "unknown";
}

function isRateLimited(ip) {
  const now = Date.now();
  const current = rateLimitStore.get(ip) || { count: 0, resetAt: now + RATE_LIMIT_WINDOW_MS };

  if (now > current.resetAt) {
    rateLimitStore.set(ip, { count: 1, resetAt: now + RATE_LIMIT_WINDOW_MS });
    return false;
  }

  current.count += 1;
  rateLimitStore.set(ip, current);
  return current.count > RATE_LIMIT_MAX;
}

async function readBody(req) {
  const chunks = [];

  for await (const chunk of req) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }

  const rawBody = Buffer.concat(chunks).toString("utf8");
  if (!rawBody) return {};

  try {
    return JSON.parse(rawBody);
  } catch {
    return null;
  }
}

async function sendResendEmail(payload) {
  return fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
}

async function saveContactSubmission(payload) {
  const supabaseConfig = getSupabaseConfig();
  if (!supabaseConfig.url || !supabaseConfig.key) {
    throw new Error(
      "Supabase is not configured. Add SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY or SUPABASE_ANON_KEY environment variables."
    );
  }

  if (!isSupabaseUrl(supabaseConfig.url)) {
    throw new Error("SUPABASE_URL must look like https://your-project-ref.supabase.co.");
  }

  const baseUrls = [supabaseConfig.url];
  const apiKeys = [supabaseConfig.key];
  const fullContactRow = {
    accepted_terms: payload.accepted_terms,
    email: payload.email,
    ip_address: payload.ip_address,
    message: payload.message,
    name: payload.name,
    source: payload.source,
    subject: payload.subject,
    user_agent: payload.user_agent,
  };
  const basicContactRow = {
    email: payload.email,
    message: payload.message,
    name: payload.name,
    subject: payload.subject,
  };
  const minimalContactRow = {
    email: payload.email,
    message: payload.message,
    name: payload.name,
  };

  const targetTables = Array.from(new Set([SUPABASE_CONTACT_TABLE, "contacts"]));

  const postRow = async (baseUrl, apiKey, tableName, row) => {
    const response = await fetch(`${baseUrl}/rest/v1/${tableName}`, {
      method: "POST",
      headers: {
        apikey: apiKey,
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        Prefer: "return=minimal",
      },
      body: JSON.stringify(row),
    });

    if (response.ok) return;

    const detail = await response.text().catch(() => "");
    throw new Error(detail || "Supabase insert failed.");
  };

  const saveToTable = async (baseUrl, apiKey, tableName) => {
    try {
      await postRow(baseUrl, apiKey, tableName, fullContactRow);
    } catch (error) {
      const detail = String(error.message || "");
      const looksLikeMissingColumn =
        detail.includes("PGRST204") ||
        detail.toLowerCase().includes("schema cache") ||
        detail.toLowerCase().includes("column");

      if (!looksLikeMissingColumn) throw error;

      try {
        await postRow(baseUrl, apiKey, tableName, basicContactRow);
      } catch (basicError) {
        const basicDetail = String(basicError.message || "");
        const subjectLooksMissing =
          basicDetail.includes("PGRST204") ||
          basicDetail.toLowerCase().includes("schema cache") ||
          basicDetail.toLowerCase().includes("subject");

        if (!subjectLooksMissing) throw basicError;
        await postRow(baseUrl, apiKey, tableName, minimalContactRow);
      }
    }
  };

  const savedTables = [];
  const errors = [];

  for (const baseUrl of baseUrls) {
    for (const apiKey of apiKeys) {
      for (const tableName of targetTables) {
        try {
          await saveToTable(baseUrl, apiKey, tableName);
          savedTables.push(tableName);
        } catch (error) {
          errors.push(`${baseUrl}/${tableName}: ${error.message}`);
        }
      }

      if (savedTables.length) {
        return { tables: savedTables };
      }
    }
  }

  if (!savedTables.length) {
    throw new Error(errors.join(" | ") || "Supabase insert failed.");
  }
  return { tables: savedTables };
}

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return sendJson(res, 405, { message: "Method not allowed." });
  }

  if (ALLOWED_ORIGIN) {
    const origin = req.headers.origin || "";
    if (origin !== ALLOWED_ORIGIN) {
      return sendJson(res, 403, { message: "This request is not allowed." });
    }
  }

  const clientIp = getClientIp(req);
  if (isRateLimited(clientIp)) {
    return sendJson(res, 429, {
      message: "Too many messages. Please wait a minute and try again.",
    });
  }

  const body = await readBody(req);
  if (!body) {
    return sendJson(res, 400, { message: "Invalid request body." });
  }

  const name = cleanText(body.name, 120);
  const email = cleanText(body.email, 180).toLowerCase();
  const subject = cleanText(body.subject, 160) || "Website enquiry";
  const message = cleanText(body.message, 4000);
  const acceptedTerms = Boolean(body.terms);
  const company = cleanText(body.company, 200);

  if (company) {
    return sendJson(res, 200, { message: "Message received." });
  }

  if (!name || !email || !message || !acceptedTerms) {
    return sendJson(res, 400, {
      message: "Please fill name, email, message, and accept the policy.",
    });
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return sendJson(res, 400, { message: "Please enter a valid email address." });
  }

  const submittedAt = new Date().toLocaleString("en-IN", {
    timeZone: "Asia/Kolkata",
    dateStyle: "medium",
    timeStyle: "short",
  });

  const safeName = escapeHtml(name);
  const safeEmail = escapeHtml(email);
  const safeSubject = escapeHtml(subject);
  const safeMessage = escapeHtml(message).replace(/\n/g, "<br />");
  const safeSubmittedAt = escapeHtml(submittedAt);

  let savedToSupabase = false;

  try {
    const saveResult = await saveContactSubmission({
      name,
      email,
      subject,
      message,
      accepted_terms: acceptedTerms,
      source: "website-contact-form",
      user_agent: cleanText(req.headers["user-agent"] || "", 500),
      ip_address: cleanText(clientIp, 120),
    });
    savedToSupabase = Boolean(saveResult.tables?.length);
  } catch (error) {
    console.error("Supabase contact submission failed:", error);
    return sendJson(res, 502, {
      message: "Could not save your message right now. Please try again later.",
      detail: getPublicErrorMessage(error),
    });
  }

  const adminText = [
    "New website enquiry",
    "",
    `Name: ${name}`,
    `Email: ${email}`,
    `Subject: ${subject}`,
    `Submitted: ${submittedAt}`,
    "",
    "Message:",
    message,
  ].join("\n");

  const userText = [
    `Hi ${name},`,
    "",
    "Thank you for reaching out to Sarvesh Mopkar.",
    "Your message has been received. We usually reply within 24 hours.",
    "",
    "Your submitted message:",
    message,
    "",
    "Warmly,",
    "Sarvesh Mopkar",
  ].join("\n");

  const emailShellStart = `
    <div style="margin:0;padding:0;background:#f7f1e8;font-family:Arial,sans-serif;color:#201a12">
      <div style="max-width:680px;margin:0 auto;padding:28px 16px">
        <div style="overflow:hidden;border:1px solid #d8b978;border-radius:18px;background:#fffaf3;box-shadow:0 18px 46px rgba(61,40,12,.12)">
          <div style="padding:26px 30px;background:#241b12;color:#fff8eb">
            <p style="margin:0 0 8px;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:#d6a950">Sarvesh Mopkar</p>
            <h1 style="margin:0;font-family:Georgia,serif;font-weight:400;font-size:30px;line-height:1.15;color:#fff8eb">`;

  const emailShellMiddle = `</h1>
          </div>
          <div style="padding:28px 30px;line-height:1.65">`;

  const emailShellEnd = `
          </div>
          <div style="padding:18px 30px;border-top:1px solid #ead8bb;background:#fff5e4;color:#6f5531;font-size:13px">
            Wealth. Consciousness. Alignment.
          </div>
        </div>
      </div>
    </div>`;

  const adminHtml = `${emailShellStart}New website enquiry${emailShellMiddle}
      <div style="display:grid;gap:10px;margin-bottom:22px">
        <p style="margin:0"><strong>Name:</strong> ${safeName}</p>
        <p style="margin:0"><strong>Email:</strong> <a style="color:#b67811" href="mailto:${safeEmail}">${safeEmail}</a></p>
        <p style="margin:0"><strong>Subject:</strong> ${safeSubject}</p>
        <p style="margin:0"><strong>Submitted:</strong> ${safeSubmittedAt}</p>
      </div>
      <div style="padding:20px;border:1px solid #ead8bb;border-radius:14px;background:#fffdf8">
        <p style="margin:0 0 10px;color:#8b5b12;font-weight:700">Message</p>
        <p style="margin:0">${safeMessage}</p>
      </div>
    ${emailShellEnd}`;

  const userHtml = `${emailShellStart}Message received${emailShellMiddle}
      <p style="margin:0 0 16px">Hi ${safeName},</p>
      <p style="margin:0 0 16px">Thank you for reaching out. Your message has been received, and we usually reply within 24 hours.</p>
      <div style="padding:20px;border:1px solid #ead8bb;border-radius:14px;background:#fffdf8">
        <p style="margin:0 0 10px;color:#8b5b12;font-weight:700">Your submitted message</p>
        <p style="margin:0">${safeMessage}</p>
      </div>
      <p style="margin:22px 0 0">Warmly,<br />Sarvesh Mopkar</p>
    ${emailShellEnd}`;

  if (!process.env.RESEND_API_KEY) {
    console.warn("Resend email skipped: RESEND_API_KEY is not configured.");
    return sendJson(res, 200, {
      message: "Thank you. Your message has been received successfully.",
      saved: savedToSupabase,
      emailed: false,
    });
  }

  const adminEmailResponse = await sendResendEmail({
    from: FROM_EMAIL,
    to: [TO_EMAIL],
    reply_to: email,
    subject: `New enquiry: ${subject}`,
    html: adminHtml,
    text: adminText,
  });

  if (!adminEmailResponse.ok) {
    const detail = await adminEmailResponse.text().catch(() => "");
    console.error("Admin email failed:", detail);

    return sendJson(res, 200, {
      message:
        "Your message has been received. The email notification could not be delivered, but we saved your enquiry.",
      saved: savedToSupabase,
      emailed: false,
    });
  }

  const autoReplyResponse = await sendResendEmail({
    from: FROM_EMAIL,
    to: [email],
    reply_to: TO_EMAIL,
    subject: "We received your message - Sarvesh Mopkar",
    html: userHtml,
    text: userText,
  });

  if (!autoReplyResponse.ok) {
    const detail = await autoReplyResponse.text().catch(() => "");
    console.error("Auto reply email failed:", detail);

    return sendJson(res, 200, {
      message:
        "Your message has been sent. The confirmation email could not be delivered, but we received your enquiry.",
      saved: savedToSupabase,
    });
  }

  return sendJson(res, 200, {
    message: "Thank you. Your message has been sent successfully.",
    saved: savedToSupabase,
  });
};
