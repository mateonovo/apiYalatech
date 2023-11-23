document.addEventListener("DOMContentLoaded", function() {
    const openButton = document.getElementById("openButton");
    const updateButton = document.getElementById("updateButton");
    const messageElement = document.getElementById("message"); // Elemento para mostrar el mensaje
    const productList = document.getElementById("actualizados");
    

    updateButton.addEventListener("click", function() {
        // Lógica para actualizar precios usando Fetch API
        fetch("/update", {
            method: "POST"
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.message); // Imprimir mensaje del servidor
            showMessage(messageElement, data.message); // Muestra el mensaje en pantalla
    
            if (data.actualizados && data.actualizados.length > 0) {
                const productListElement = document.getElementById("actualizados");
                productListElement.innerHTML = "Productos actualizados:<br>";
    
                data.actualizados.forEach(product => {
                    const productElement = document.createElement("div");
                    productElement.className = "product";
        
                    const productInfo = document.createElement("p");
                    productInfo.innerHTML = `<strong>Nombre:</strong> ${product.name}<br><strong>Código de Barras:</strong> ${product.barCode}<br><strong>Precio:</strong> ${product.price}`;
                    
                    productElement.appendChild(productInfo);
                    productList.appendChild(productElement);
                    
                });
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
    

    function showMessage(element, message) {
        element.textContent = message; // Establece el mensaje
        element.style.backgroundColor = "#007bff"; // Establece el color de fondo
        element.style.opacity = 4; // Muestra el mensaje
        element.style.transition = "opacity 0.5s ease-in-out"; // Animación de entrada
        element.style.color="white";
        // Borra el mensaje después de 2 segundos
        setTimeout(function() {
            element.textContent = "";
            element.style.opacity = 0;
        }, 8000);
    }
});
