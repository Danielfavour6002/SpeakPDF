const paymentForm = document.getElementById('paymentForm');
paymentForm.addEventListener("submit", payWithPaystack, false);

function payWithPaystack(e) {
    e.preventDefault();

    let handler = PaystackPop.setup({
        key: 'pk_live_34d4bc1cc542a5b69b25e87854ffa7add717ae57', // Replace with your public key
        email: document.getElementById("email-address").value,
        amount: document.getElementById("amount").value * 100, // Convert Naira to Kobo
        currency: 'NGN', // Set currency to Naira
        ref: ''+Math.floor((Math.random() * 1000000000) + 1), // generates a pseudo-unique reference. Please replace with a reference you generated. Or remove the line entirely so our API will generate one for you
        onClose: function(){
            alert('Window closed.');
        },
        callback: function(response){
            let message = 'Payment complete! Reference: ' + response.reference;
            alert(message);
            window.location.href = "/"; // Redirect to the home page
        }
    });

    handler.openIframe();
}
