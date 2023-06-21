console.log('hello world')


// Get necessary elements from the DOM
const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

const url = window.location.href

// Add click event listeners to modal buttons
modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    
    // Get data attributes from the clicked button
    const pk = modalBtn.getAttribute('data-pk')
    const name = modalBtn.getAttribute('data-quiz')
    const numQuestions = modalBtn.getAttribute('data-questions')
    const difficulty = modalBtn.getAttribute('data-difficulty')
    const scoreToPass = modalBtn.getAttribute('data-pass')
    const time = modalBtn.getAttribute('data-time')

    // Populate the modal body with confirmation details
    modalBody.innerHTML = `
        <div class="h5 mb-3">Are you sure you want to begin "<b>${name}</b>"?</div>
        <div class="text-muted">
            <ul>
                <li>difficulty: <b>${difficulty}</b></li>
                <li>number of questions: <b>${numQuestions}</b></li>
                <li>score to pass: <b>${scoreToPass}%</b></li>
                <li>time: <b>${time} min</b></li>
            </ul>
        </div>
    `

    // Add click event listener to the start button
    startBtn.addEventListener('click', ()=>{

        // Redirect to the quiz URL when start button is clicked
        window.location.href = url + pk
    })
}))