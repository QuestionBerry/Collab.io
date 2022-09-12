var loginShown = false
var regShown = false
disable_form(document.getElementById('register_form'))
disable_form(document.getElementById('login_form'))

function showHide(formName){
    var login = document.getElementById('login');
    var register = document.getElementById('register')
    
    if(formName == 'login'){
        if(!loginShown){
            if(regShown){
                register.style.height = '0px';
                register.style.opacity = 0;
                register.style.zIndex = 0;
                disable_form(document.getElementById('register_form'))
                regShown = false;
            }
            login.style.height = '50px';
            login.style.opacity = 1;
            login.style.zIndex = 20;
            enable_form(document.getElementById('login_form'))
            loginShown = true;
        } else {
            login.style.height = '0px';
            login.style.opacity = 0;
            disable_form(document.getElementById('login_form'))
            loginShown = false;
        }
    } else {
        if(!regShown){
            if(loginShown){
                login.style.height = '0px';
                login.style.opacity = 0;
                disable_form(document.getElementById('login_form'))
                loginShown = false;
            }
            register.style.height = '150px';
            register.style.opacity = 1;
            register.style.zIndex = 20;
            enable_form(document.getElementById('register_form'))
            regShown = true;
        }
        else {
            register.style.height = '0px';
            register.style.opacity = 0;
            register.style.zIndex = 0;
            disable_elements(document.getElementById('register_form'))
            regShown = false;
        }
    }
}

//Disable a form; even when opacity and height 0, they were still clickable
function disable_form(form) {
    var inputs = form.getElementsByTagName('input'),
        textareas = form.getElementsByTagName('textarea'),
        buttons = form.getElementsByTagName('button'),
        selects = form.getElementsByTagName('select');

    disable_elements(inputs);
    disable_elements(textareas);
    disable_elements(buttons);
    disable_elements(selects);
}
  // Disables a collection of form-elements.
function disable_elements(elements) {
    var length = elements.length;
    while(length--) {
        elements[length].disabled = true;
    }
}

function enable_form(form) {
    var inputs = form.getElementsByTagName('input'),
        textareas = form.getElementsByTagName('textarea'),
        buttons = form.getElementsByTagName('button'),
        selects = form.getElementsByTagName('select');

    enable_elements(inputs);
    enable_elements(textareas);
    enable_elements(buttons);
    enable_elements(selects);
}
  // Enable a collection of form-elements.
function enable_elements(elements) {
    var length = elements.length;
    while(length--) {
        elements[length].disabled = false;
    }
}