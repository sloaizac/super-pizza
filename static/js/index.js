document.addEventListener('DOMContentLoaded', () => {
    getShoppingList();
    const menuNavbar = document.querySelector('#menu-navbar');
    document.querySelectorAll('section').forEach(section => {
        const a = document.createElement('a');
        a.href = "#" + section.id;
        a.innerHTML = section.id;
        a.classList.add("m-2");
        menuNavbar.append(a);
    });

    document.querySelectorAll('td').forEach(td => {
        td.onclick = () => {
            const item = {
                id: td.parentElement.dataset.info,
                category: td.parentElement.parentElement.dataset.type,
                name: td.parentElement.firstElementChild.innerHTML,
                price: td.innerHTML,
                size: td.dataset.size
            }

            const request = new XMLHttpRequest();
            request.open('POST', '/add-item/');
            request.onload = () => {
                if (request.status == 200) {
                    getShoppingList();
                }
            }

            const data = new FormData();
            data.append('item', JSON.stringify(item));
            request.send(data);
        }

    });

})

function getShoppingList() {
    const request = new XMLHttpRequest();
    request.open('POST', '/get-shopping-list/');
    request.onload = () => {
        if (request.status == 403) {
            document.querySelector('#shopping-list').innerHTML = 'No tiene productos aún';
        } else {
            const data = JSON.parse(request.responseText)
            document.querySelector('#item-count').innerHTML = data.response.length;
            const ul = document.querySelector('#list');
            const total =  document.querySelector('#total');
            total.innerHTML = 0;
            data.response.forEach((i) => {
                const item = JSON.parse(i);
                addItem(ul, item, total);
            });
        }
    }

    const data = new FormData();
    request.send(data);
}

function addItem(ul, item, total) {
    const li = document.createElement('li');
    const span = document.createElement('span'); 
    li.innerHTML = item.category + ' ' + item.name + ' ' + item.size;
    span.innerHTML = '$' + item.price;
    if (parseInt(item.name[0])){
        console.log(parseInt(item.name[0]));  
    }
    span.classList.add('float-right');
    li.classList.add('list-group-item');
    li.append(span);
    ul.append(li);
    total.innerHTML = parseFloat(total.innerHTML) + parseFloat(item.price);   
}

function showList() {
    var list = document.getElementById("shopping-list");
    if (list.style.display === "none") {
        list.style.display = "block";
    } else {
        list.style.display = "none";
    }
}
