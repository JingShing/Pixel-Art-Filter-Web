const pixel_set_vars = ["k","scale","blur","erode","saturation","contrast","qr_code_content", "original_img_src", "result_img_src"]
const session_set = ["user_key", "user_secret_key"]
const pixel_checkbox = ["alpha", "to_tw", "qr_code"]
function save_pixel_set_to_local_storage(){
    for(let i = 0;i<pixel_set_vars.length;i++)localStorage.setItem(pixel_set_vars[i], document.getElementById(pixel_set_vars[i]).value);
    for(let i = 0;i<pixel_checkbox.length;i++)localStorage.setItem(pixel_checkbox[i], document.getElementById(pixel_checkbox[i]).checked);
    for(let i = 0;i<session_set.length;i++)sessionStorage.setItem(session_set[i], document.getElementById(session_set[i]).value);
}
function load_pixel_set_to_local_storage(){
    for(let i = 0;i<pixel_set_vars.length;i++)if(localStorage.getItem(pixel_set_vars[i]))document.getElementById(pixel_set_vars[i]).value=localStorage.getItem(pixel_set_vars[i])
    for(let i = 0;i<pixel_checkbox.length;i++){
        if(localStorage.getItem(pixel_checkbox[i])=='true')document.getElementById(pixel_checkbox[i]).checked=localStorage.getItem(pixel_checkbox[i])
        else document.getElementById(pixel_checkbox[i]).removeAttribute("checked");
    }
    qr_code_enable();
    for(let i = 0;i<session_set.length;i++)document.getElementById(session_set[i]).value = sessionStorage.getItem(session_set[i]);
}
function qr_code_enable(){
    if(document.getElementById('qr_code').checked==true){
        document.getElementById('qr_code_content').removeAttribute("hidden");
        document.getElementById('qr_code_content_hint').removeAttribute("hidden");
    }
    else{
        document.getElementById('qr_code_content').setAttribute("hidden", "hidden");
        document.getElementById('qr_code_content_hint').setAttribute("hidden", "hidden");
    }
}
window.addEventListener('change', save_pixel_set_to_local_storage, false)
window.addEventListener('load', load_pixel_set_to_local_storage, false)