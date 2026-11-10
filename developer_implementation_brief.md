# Developer Task Brief — Cambridge Care Services

**Target Website:** `cambridgecareservices.co.uk` (Next.js)  
**Estimated Developer Effort:** ~20 to 30 minutes  
**Contact / Registered Manager:** +44 7917 611 425

---

## Overview

Please implement the following two lightweight additions to the Cambridge Care Services website:
1. **Task 1:** Add the 1-line script for the Floating AI Care Assistant Widget.
2. **Task 2:** Add Twilio WhatsApp dispatch logic to the existing contact / assessment form handler.

---

## Task 1: Embed AI Care Assistant Widget (1 Minute)

Place this single script tag **immediately before the closing `</body>` tag** in your root layout (`app/layout.tsx` or main HTML template):

```html
<script src="https://cdn.jsdelivr.net/gh/pankajatd/cambridge-care-chatbot@main/widget.js" async></script>
```

*(If using Next.js `<Script>` component):*

```tsx
import Script from 'next/script';

// Inside your root layout:
<Script 
  src="https://cdn.jsdelivr.net/gh/pankajatd/cambridge-care-chatbot@main/widget.js" 
  strategy="lazyOnload" 
/>
```

---

## Task 2: Automated WhatsApp Alert on Form Submission (20 Minutes)

When a prospective client or hospital discharge team submits a care inquiry form, dispatch an instant WhatsApp alert to the Registered Manager.

### Step 1: Install Twilio SDK
```bash
npm install twilio
```

### Step 2: Environment Variables
Add these keys to your `.env.local` (and in your production hosting dashboard, e.g. Vercel):

```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_WHATSAPP_SENDER=whatsapp:+14155238886
CARE_MANAGER_WHATSAPP_NUMBER=whatsapp:+447917611425
```

### Step 3: Backend API Route Code
Add the following dispatch logic to your form submission endpoint (e.g. `app/api/contact/route.ts`):

```typescript
import { NextResponse } from 'next/server';
import twilio from 'twilio';

const client = twilio(process.env.TWILIO_ACCOUNT_SID, process.env.TWILIO_AUTH_TOKEN);
const twilioSender = process.env.TWILIO_WHATSAPP_SENDER || 'whatsapp:+14155238886';
const managerPhone = process.env.CARE_MANAGER_WHATSAPP_NUMBER || 'whatsapp:+447917611425';

export async function POST(request: Request) {
  try {
    const data = await request.json();
    const { fullName, phone, email, postcode, careType, schedule, startDate, notes } = data;

    // 1. Compose formatted WhatsApp message
    const alertMessage = 
      `🚨 *NEW CARE INQUIRY — Cambridge Care Services*\n\n` +
      `👤 *Contact:* ${fullName || 'Not provided'}\n` +
      `📞 *Phone:* ${phone || 'Not provided'}\n` +
      `📧 *Email:* ${email || 'Not provided'}\n` +
      `📍 *Location:* ${postcode || 'Cambridge / South Cambs'}\n` +
      `🩺 *Care Needs:* ${careType || 'General Care'}\n` +
      `⏰ *Schedule:* ${schedule || 'Flexible'}\n` +
      `📅 *Start Date:* ${startDate || 'ASAP'}\n` +
      `💬 *Notes:* ${notes || 'None'}\n\n` +
      `👉 *Tap phone number to call family immediately.*`;

    // 2. Dispatch WhatsApp alert
    await client.messages.create({
      from: twilioSender,
      to: managerPhone,
      body: alertMessage,
    });

    return NextResponse.json({ success: true, message: 'Inquiry received and notified.' });
  } catch (error: any) {
    console.error('WhatsApp notification error:', error);
    // Return 200 so form submission still succeeds for user even if notification encounters an issue
    return NextResponse.json({ success: true, warning: 'Saved without notification' }, { status: 200 });
  }
}
```

---

## Verification & Acceptance Criteria

- [ ] Floating circular `🌸` button appears in the bottom-right corner of the website.
- [ ] Clicking the bubble opens the Cambridge Care Assistant window cleanly.
- [ ] Submitting a test form on the website successfully delivers a formatted WhatsApp alert to `+44 7917 611 425`.
