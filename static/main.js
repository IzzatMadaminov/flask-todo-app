const checkboxes = document.querySelectorAll('.check-completed');
for(let i = 0; i < checkboxes.length; i++) {
    const checkbox = checkboxes[i];
    checkbox.onchange = function(e) {
        console.log("event ", e)
        const todoid = e.target.dataset['id'];
        const newCompleted = e.target.checked;
        fetch('/todos/' + todoid + '/set-completed', {
            method: 'POST',
            body: JSON.stringify({
                'completed': newCompleted
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        })
    }
}
const buttons = document.querySelectorAll('.delete-button');
for(let i = 0; i < buttons.length; i++) {
    const button = buttons[i];
    button.onclick = function() {
        const todoid = this.dataset['id'];
        fetch('/todos/' + todoid, {
            method: 'DELETE'
        })
        .then((resp) => this.parentElement.remove())
        .catch(function(error) {
        console.log(error);
        })
    }
}

const list_checkboxes = document.querySelectorAll('.completed-list');
for(let i = 0; i < list_checkboxes.length; i++) {
    const checkbox = list_checkboxes[i];
    checkbox.onchange = function(e) {
        const listid = e.target.dataset['id'];
        const newCompleted = e.target.checked;
        fetch('/lists/' + listid + '/set-completed', {
            method: 'POST',
            body: JSON.stringify({
                'completed': newCompleted
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then((resp) => {
            for(let i = 0; i < checkboxes.length; i++) {
                let checkbox = checkboxes[i];
                if(checkbox.dataset['listId'] == listid) {
                    checkbox.checked = newCompleted;
                }
            }
        })
    }
}
const list_buttons = document.querySelectorAll('.delete-list');
for(let i = 0; i < list_buttons.length; i++) {
    const button = list_buttons[i];
    button.onclick = function() {
        const todoid = this.dataset['id'];
        fetch('/lists/' + todoid, {
            method: 'DELETE'
        })
        .then((resp) => this.parentElement.remove())
        .catch(function(error) {
        console.log(error);
        })
    }
}