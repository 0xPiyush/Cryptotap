var claimForm = document.getElementById('claim-form');

claimForm.addEventListener('submit', function (event) {
    const button = document.getElementById('get-crypto-btn')
    button.disabled = true;
    event.preventDefault();
    var formData = new FormData(claimForm)
    var validAddr = WAValidator.validate(formData.get('wallet-addr'), coin);

    addDataToForm(claimForm, {'valid-addr': validAddr}).submit()
});

function addDataToForm(form, data) {
    if(typeof form === 'string') {
        if(form[0] === '#') form = form.slice(1);
        form = document.getElementById(form);
    }

    var keys = Object.keys(data);
    var name;
    var value;
    var input;

    for (var i = 0; i < keys.length; i++) {
        name = keys[i];
        // removing the inputs with the name if already exists [overide]
        // console.log(form);
        Array.prototype.forEach.call(form.elements, function (inpt) {
             if(inpt.name === name) {
                 inpt.parentNode.removeChild(inpt);
             }
        });

        value = data[name];
        input = document.createElement('input');
        input.setAttribute('name', name);
        input.setAttribute('value', value);
        input.setAttribute('type', 'hidden');

        form.appendChild(input);
    }

    return form;
}