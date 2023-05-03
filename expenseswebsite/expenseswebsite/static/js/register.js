const usernameField = document.querySelector('#usernameField');
const feedbackArea = document.querySelector(".invalid_feedback");
const emailField = document.querySelector("#emailField");
const emailFeedbackArea = document.querySelector(".emailFeedbackArea");
const passwordField = document.querySelector("#passwordField");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const submitBtn = document.querySelector(".submit-btn")

const handleToggleInput=(e)=>{
    if (showPasswordToggle.textContent==='SHOW'){
        showPasswordToggle.textContent = 'HIDE';
        
        passwordField.setAttribute("type", "text");


    }else{
        showPasswordToggle.textContent = 'SHOW';

        passwordField.setAttribute("type", "password");

    }
};

showPasswordToggle.addEventListener("click", handleToggleInput);

emailField.addEventListener('keyup', (e) => {
    const emailval = e.target.value;

    emailField.classList.remove("is-invalid");
    emailFeedbackArea.style.display = "none";


    if (emailval.length > 0) {
        fetch("/authentication/validate-email",{
            body: JSON.stringify({ email: emailval }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data",data);
                if (data.email_error){
                    submitBtn.disabled= true;
                    emailField.classList.add("is-invalid");
                    feedbackArea.style.display = "block";
                    emailFeedbackArea.innerHTML = `<p>${data.email_error}</p>`;
                }else{
                    submitBtn.disabled= false;

                }
            });
    }
});


usernameField.addEventListener("keyup", (e) => {

    const usernameval = e.target.value;
    usernameField.classList.remove("is-invalid");
    feedbackArea.style.display = "none";


    if (usernameval.length > 0) {
        fetch("/authentication/validate-username",{
            body: JSON.stringify({ username: usernameval }),
            method: "POST",
        })
            .then((res) => res.json())
            .then((data) => {
                console.log("data",data);
                if (data.username_error){
                    submitBtn.disabled= true;
                    usernameField.classList.add("is-invalid");
                    feedbackArea.style.display = "block";
                    feedbackArea.innerHTML = `<p>${data.username_error}</p>`;
                }else{
                    submitBtn.disabled= false;

                }
            });
    }
});
