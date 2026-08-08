async function handleInquirySubmit(event) {
    event.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    const name = document.getElementById('custName').value;
    const contact = document.getElementById('custContact').value;
    const inquiryType = document.getElementById('inquiryType').value;
    const message = document.getElementById('custMessage').value;

    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i> Sending...';

    try {
        // Send email request via Flask API
        const response = await fetch('/api/inquiry', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, contact, inquiryType, message })
        });
        const resData = await response.json();
        
        console.log('Server response:', resData);
    } catch (err) {
        console.warn('Network log:', err);
    } finally {
        submitBtn.innerHTML = '<i class="fa-solid fa-paper-plane mr-2"></i> Send Email & WhatsApp Inquiry';
    }

    // Trigger immediate WhatsApp redirection
    const waText = `*NEW INQUIRY - ONE TRADE*\n` +
                   `*Name:* ${name}\n` +
                   `*Contact:* ${contact}\n` +
                   `*Type:* ${inquiryType}\n` +
                   `*Message:* ${message || 'N/A'}\n` +
                   `*Location:* Bijwar, Sitapur, UP`;

    window.open(`https://wa.me/919795650090?text=${encodeURIComponent(waText)}`, '_blank');
}

function requestCallback() {
    const phone = prompt("Enter your 10-digit mobile number for a call back from ONE TRADE:");
    if (phone && phone.trim().length >= 10) {
        const waText = `*CALLBACK REQUEST*\nPlease call me back at: ${phone.trim()} for TMT Sariya pricing.`;
        window.open(`https://wa.me/919795650090?text=${encodeURIComponent(waText)}`, '_blank');
    }
}

function openDirections() {
    // Exact location query pin for Bijwar, Sitapur, UP 261001
    const mapsUrl = "https://www.google.com/maps/search/?api=1&query=Bijwar+Sitapur+Uttar+Pradesh+261001";
    window.open(mapsUrl, '_blank');
}