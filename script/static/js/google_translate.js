function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'en'}, 'google_translate_element');
}
function need_translate(){
    sessionStorage.setItem('need_translate', 'true');
    document.getElementById('google_translate_element').hidden=false;
    document.getElementById('other_lang_s').hidden=true;
    googleTranslateElementInit();
    de_logo()
}
function de_logo(){
    var parent = document.getElementById(':0.targetLanguage').parentNode;
    if(parent.childNodes.length>1){
        parent.removeChild(parent.lastElementChild);
        parent.removeChild(parent.lastChild);
        parent.removeChild(parent.lastChild);
    }
}
function translate_init(){
    if(sessionStorage.getItem('need_translate')=='true'){
        need_translate();
        de_logo();
    }
    else document.getElementById('other_lang').addEventListener('click', need_translate, false);
}
window.addEventListener('load', translate_init, false);