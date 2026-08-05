/*** Dark Mode ***
  Purpose:
  - Toggles the website theme between light and dark mode.
***/
const themeButton = document.getElementById("theme-button");

const toggleDarkMode = () => {
  document.body.classList.toggle("dark-mode");
}

if (themeButton) {
  themeButton.addEventListener("click", toggleDarkMode);
}


/*** Scroll Animations ***
  Purpose:
  - Animates site sections fading and moving into view when scrolling.
***/
const reveal = () => {
  let revealables = document.querySelectorAll(".revealable");
  for (let i = 0; i < revealables.length; i++) {
    let windowHeight = window.innerHeight;
    let topOfRevealable = revealables[i].getBoundingClientRect().top;
    let revealPoint = 150;

    if (topOfRevealable < windowHeight - revealPoint) {
      revealables[i].classList.add("active");
    } else {
      revealables[i].classList.remove("active");
    }
  }
}

window.addEventListener("scroll", reveal);


/*** Form Handling ***
  Purpose:
  - Adds participant to the RSVP list.
***/
const addParticipant = (person) => {
  const participantList = document.getElementById("participant-list");
  const newListItem = document.createElement("li");
  newListItem.textContent = `${person.name} (${person.state})`;
  participantList.appendChild(newListItem);
  
  // Stretch Feature: Live RSVP counter update
  const rsvpCountSpan = document.getElementById("rsvp-count");
  if (rsvpCountSpan) {
    let currentCount = parseInt(rsvpCountSpan.textContent) || 0;
    rsvpCountSpan.textContent = currentCount + 1;
  }
}


/*** Form Validation ***
  Purpose:
  - Prevents invalid form submissions from being added to the list of participants.
***/
const validateForm = () => {
  let containsErrors = false;
  var rsvpInputs = document.getElementById("rsvp-form").elements;

  // Loop through all inputs (excluding the submit button)
  for (let i = 0; i < rsvpInputs.length; i++) {
    if (rsvpInputs[i].type !== "button") {
      if (rsvpInputs[i].value.trim().length < 2) {
        containsErrors = true;
        rsvpInputs[i].classList.add("error");
      } else {
        rsvpInputs[i].classList.remove("error");
      }
    }
  }

  // Stretch Feature: Specific validation for email address
  const emailInput = document.getElementById("email");
  if (emailInput) {
    if (!emailInput.value.includes("@")) {
      containsErrors = true;
      emailInput.classList.add("error");
    }
  }

  let person = {
    name: document.getElementById("name").value,
    state: document.getElementById("state").value,
    email: document.getElementById("email").value
  };

  // If no errors, call addParticipant() and clear fields
  if (containsErrors === false) {
    addParticipant(person);
    toggleModal(person);
    
    // Clear all inputs and remove error border indicators
    for (let i = 0; i < rsvpInputs.length; i++) {
      if (rsvpInputs[i].type !== "button") {
        rsvpInputs[i].value = "";
      }
      rsvpInputs[i].classList.remove("error");
    }
  }
}

// Add event listener to form button
const rsvpButton = document.getElementById("rsvp-button");
if (rsvpButton) {
  rsvpButton.addEventListener("click", validateForm);
}


/*** Success Modal ***
  Purpose:
  - Display personalized modal and animate image on valid RSVP submission.
***/
const toggleModal = (person) => {
  let modal = document.getElementById("success-modal");
  let modalText = document.getElementById("modal-text");

  modal.style.display = "flex";
  modalText.textContent = `Thanks for RSVPing, ${person.name}! We can't wait to see you at the event!`;

  let intervalId = setInterval(animateImage, 500);

  setTimeout(() => {
    modal.style.display = "none";
    clearInterval(intervalId);
  }, 5000);
}

let rotateFactor = 0;
let modalImage = document.getElementById("modal-img");

const animateImage = () => {
  if (rotateFactor === 0) {
    rotateFactor = -10;
  } else {
    rotateFactor = 0;
  }
  if (modalImage) {
    modalImage.style.transform = `rotate(${rotateFactor}deg)`;
  }
}
