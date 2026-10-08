const drop_down = document.getElementById("file_selector")
const user_question = document.getElementById("question")
const button = document.getElementById("question_submit")
const ai_answer = document.getElementById("answer_from_ai")
const upload_button = document.getElementById("upload-button")
const user_file = document.getElementById("file-uploads")
const file_upload_feedback = document.getElementById("file-upload-feedback")
const subject = document.getElementById("subject")

upload_button.addEventListener("click",upload_file)

async function load_files() {
    try {
        const response = await fetch("http://127.0.0.1:8000/files")
        const data = await response.json()
        
        if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
        
    }
        return data.known_files || []
        
    } catch (error) {

        console.log(error)
        return []
    } 
}

function add_to_dropdown(file) {

    drop_down.replaceChildren()

    if (file.length === 0){
        drop_down.innerHTML = `<option> No file is available </option>`;
        return;
    }
    drop_down.innerHTML = `<option selected value="">select file</option>`
    for (const item of file) {

        const op = document.createElement('option')
        op.value = item.filename
        op.textContent = item.filename
            
        console.log(item.filename)
        console.log(op.value)

        drop_down.appendChild(op)
            
        }
    
}


async function send_question() {
    let data = {}
    const user_question_value = user_question.value.trim()
    const selected_file = drop_down.value

    if (!user_question_value){
        ai_answer.textContent = "Please enter a valid question"
        return 
      }
    if (selected_file === undefined || selected_file === ""){
        ai_answer.textContent = "Please select a file first!"
        return
    }
        console.log(user_question_value)
        console.log(selected_file) 
        ai_answer.textContent = "Thinking..."
    try {
        button.disabled = true
        
        const response = await fetch("http://127.0.0.1:8000/ask",{
        method:'POST',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'question':user_question_value,'file_name':selected_file})
        });

        try{

         data = await response.json()}
        
        catch(error){
            console.log(error)
        }
        if (!response.ok) {
           if(typeof data.detail === 'string'){
            ai_answer.textContent = `Error!: ${data.detail}`}
            
           else{
            ai_answer.textContent = "Something went wrong please retry.."}
        return
        }
    
        console.log(data.answer)
        if (data.answer !== undefined){
            ai_answer.textContent = data.answer}
        else{
            ai_answer.textContent = "Sorry! Something went wrong.."
            console.log("Error answer not json ")
        }
         
    
    }   
        catch (error) {
        console.log(error) 
        ai_answer.textContent = "Can't reach the server"
        return
    }
    finally{
        button.disabled = false
    }

}  


async function start_page() {
    button.addEventListener("click", send_question)
    const file = await load_files()
    add_to_dropdown(file)
}

function read_file() {
    const selected_file = user_file.files
    if (selected_file.length === 0){
        console.log("Please select a file first")
        file_upload_feedback.textContent = "Please select a file first"
        return
    }
    return selected_file[0]
}

async function upload_file() {
    const uploaded_file = read_file()
    const subject_text = subject.value.trim()
    const form_data = new FormData()
    let data = {}

    if(!uploaded_file){
        console.log("file was not selected")
        return
    }
    if((!subject_text) || (subject_text === "")){
        file_upload_feedback.textContent = "Please enter the subject first!"
        return
    }

    form_data.append("file",uploaded_file)
    form_data.append("subject",subject_text)
    file_upload_feedback.textContent = "Uploading file.."
    
    try {
        button.disabled = true
        
        const response_upload= await fetch("http://127.0.0.1:8000/upload",{
        method:'POST',
        body:form_data
        });

        try{

         data = await response_upload.json()}
        
        catch(error){
            console.log(error)
        }
        if (!response_upload.ok) {
           if(typeof data.detail === 'string'){
            file_upload_feedback.textContent = `Error!: ${data.detail}`}
            
           else{
            file_upload_feedback.textContent = "Something went wrong please retry.."}
            return
        }
        console.log(data.chunk_count)
        const loaded_files = await load_files()
        add_to_dropdown(loaded_files)  
    file_upload_feedback.textContent = "Uploaded file sucessfully."       
    }   
        catch (error) {
        console.log(error) 
        file_upload_feedback.textContent = "Can't reach the server"
        return
    }
    finally{
        button.disabled = false
    }

}  

start_page()



