let sl = []; //shopping list
getSL();
const total = document.querySelector('#total');

//put categories
const menuNavbar = document.querySelector('#menu-navbar');
document.querySelectorAll('section').forEach(section => {
    const a = document.createElement('a');
    a.href = "#" + section.id;
    a.innerHTML = section.id;
    a.classList.add("m-1");
    menuNavbar.append(a);
});

//select item
document.querySelectorAll('td').forEach(td => {
    td.onclick = () => {
        const item = {
            id: td.parentElement.dataset.info,
            category: td.parentElement.parentElement.dataset.type,
            name: td.parentElement.firstElementChild.innerHTML,
            price: td.innerHTML,
            size: td.dataset.size
        }

        if (parseInt(item.name[0])) {
            item.toppings = new Array(parseInt(item.name[0]));
        }

        const request = new XMLHttpRequest();
        request.open('POST', '/update-sl/');
        request.onload = () => {
            if (request.status == 200) {
                getSL();
            }
        }

        const data = new FormData();
        data.append('item', JSON.stringify(item));
        request.send(data);
    }

});

//show shopping list
document.querySelector('#car-button').onclick = () => {
    let list = document.getElementById("shopping-list");
    if (list.style.display != "block") {
        list.style.display = "block";
    } else {
        list.style.display = "none";
    }
}

//confirm order
document.querySelector('#btn-order').onclick = () => {
    let order = sl;
    order.push(JSON.stringify({'total': total.innerHTML}))
    let data = new FormData();
    data.append('list', JSON.stringify(order));
    fetch('http://localhost:8000/order/', {method: 'POST', body: data})
        .then(res => window.location.replace("http://localhost:8000/order/"))
        .catch(err => console.log(err))
}

function getSL() {
    const request = new XMLHttpRequest();
    request.open('POST', '/get-sl/');
    request.onload = () => {
        if (request.status == 200) {
            sl = JSON.parse(request.responseText).list;
            if(typeof sl == 'string') sl = JSON.parse(sl);
            if (sl.length > 0) writeSL();
        }
    }
    const data = new FormData();
    request.send(data);
}

function writeSL() {
    document.querySelector('#btn-order').style.display = "block";
    let count = 0;
    let buttons = '';
    let list = document.querySelector('#sl');
    list.innerHTML = '';
    sl.forEach(item => {
        buttons = '';
        item = JSON.parse(item);  
        if (parseInt(item.name[0])) {
            buttons = '<button class="btn btn-danger btn-sm mr-2" data-toggle="modal" data-target="#modal-toppings"><i class="fas fa-plus"></i></button>';
        }
        li = document.createElement('li');
        li.id = count;
        li.innerHTML = item.category + " " + item.name + " " + item.size + "<div>" + buttons + "<span>" + item.price + "</span></div>";
        li.classList.add('d-flex', 'justify-content-between', 'p-2');
        list.append(li);
        total.innerHTML = (parseFloat(total.innerHTML) + parseFloat(item.price)).toFixed(2);
        ++count;
    })
    document.querySelector('#item-count').innerHTML = count;
    document.querySelector('ul').querySelectorAll('button').forEach(btn => {
        btn.onclick = () => {
            let id = parseInt(btn.parentElement.parentElement.id);
            selectToppings(id);
        }
    })
}

function selectToppings(id){
    let item = JSON.parse(sl[id]);
    let count = 0
    let toppings = document.querySelectorAll('.topping');
    toppings.forEach(t => {
        t.onclick = () => {
            if(t.checked && count < item.toppings.length){
                item.toppings[count] = t.id;
                ++count;
            }else if(!t.checked){
                --count;
            }
        }
    });
    document.querySelector('#save-toppings').onclick = () => {
        sl[id] = JSON.stringify(item);
        toppings.forEach(t => t.checked = false);
    }
}

