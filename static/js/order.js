let order, total = document.querySelector('#total');
let list = document.querySelector('#order-list');

const request = new XMLHttpRequest();
request.open('GET', '/get-order/');
request.onload = () => {
    if (request.status == 200) {
        order = JSON.parse(JSON.parse(request.responseText).list);
        let toppings;
        order.forEach(e => {
            let item = JSON.parse(e);
            if (item.total) {
                total.innerHTML = item.total;
            } else {
                toppings = '';

                if (parseInt(item.name[0])) {
                    toppings = item.toppings;
                }
                li = document.createElement('li');
                li.innerHTML = item.category + " " + item.name + " " + item.size + " " + toppings + "<span>" + item.price + "</span>";
                li.classList.add('d-flex', 'justify-content-between', 'p-2');
                list.append(li);
            }
        });

    }
}
request.send();