document.addEventListener("DOMContentLoaded", () => {

  // === Variables y elementos ===
  const apiServicios = '/api/servicios';
  const apiProductos = '/api/productos';
  const serviceList = document.getElementById('serviceList'); // contenedor para mostrar lista de servicios
  const productList = document.getElementById('productList'); // contenedor para mostrar lista de productos
  const formServicio = document.getElementById('formServicio'); // formulario de servicios
  const formProducto = document.getElementById('formProducto'); // formulario de productos

  let editIdServicio = null; // id para editar servicio
  let editIdProducto = null; // id para editar producto

  // === Cargar listas al iniciar ===
  loadServices();
  loadProducts();

  // === FUNCIONES PARA SERVICIOS ===

  function loadServices() {
    fetch(apiServicios)
      .then(res => res.json()) // traigo todos los servicios en formato JSON
      .then(data => {
        serviceList.innerHTML = ''; // limpio el contenedor
        data.forEach(s => {
          const card = document.createElement('div'); // creo tarjeta para cada servicio
          card.style.border = '1px solid #ddd';
          card.style.padding = '10px';
          card.style.marginBottom = '10px';

          // información y botones Editar/Eliminar
          card.innerHTML = `
            <h3>${s.nombre}</h3>
            <p>${s.descripcion}</p>
            <p><strong>Precio:</strong> $${s.precio.toFixed(2)}</p>
            <button onclick="editService(${s.id}, '${s.nombre}', '${s.descripcion}', ${s.precio})">Editar</button>
            <button onclick="deleteService(${s.id})">Eliminar</button>
          `;
          serviceList.appendChild(card);
        });
      });
  }

  // === Enviar formulario SERVICIO ===
  formServicio.onsubmit = function (e) {
    e.preventDefault(); // evito recargar página
    const nombre = formServicio.querySelector('[name="nombre"]').value;
    const descripcion = formServicio.querySelector('[name="descripcion"]').value;
    const precio = parseFloat(formServicio.querySelector('[name="precio"]').value);

    const data = { nombre, descripcion, precio };

    if (editIdServicio) {
      // === Actualizar servicio existente ===
      fetch(`${apiServicios}/${editIdServicio}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(() => {
        formServicio.reset();
        editIdServicio = null;
        loadServices();
      });
    } else {
      // === Crear nuevo servicio ===
      fetch(apiServicios, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(() => {
        formServicio.reset();
        loadServices();
      });
    }
  };

  // === Editar servicio ===
  window.editService = function (id, nombre, descripcion, precio) {
    formServicio.querySelector('[name="nombre"]').value = nombre;
    formServicio.querySelector('[name="descripcion"]').value = descripcion;
    formServicio.querySelector('[name="precio"]').value = precio;
    editIdServicio = id;
  };

  // === Eliminar servicio ===
  window.deleteService = function (id) {
    if (confirm('¿Seguro que quieres eliminar este servicio?')) {
      fetch(`${apiServicios}/${id}`, { method: 'DELETE' })
        .then(() => loadServices());
    }
  };

  // === FUNCIONES PARA PRODUCTOS ===

  function loadProducts() {
    fetch(apiProductos)
      .then(res => res.json()) // traigo todos los productos en formato JSON
      .then(data => {
        productList.innerHTML = ''; // limpio el contenedor
        data.forEach(p => {
          const card = document.createElement('div'); // creo tarjeta para cada producto
          card.style.border = '1px solid #ddd';
          card.style.padding = '10px';
          card.style.marginBottom = '10px';

          // información y botones Editar/Eliminar
          card.innerHTML = `
            <h3>${p.nombre}</h3>
            <p>${p.descripcion}</p>
            <p><strong>Precio:</strong> $${p.precio.toFixed(2)}</p>
            <button onclick="editProduct(${p.id}, '${p.nombre}', '${p.descripcion}', ${p.precio})">Editar</button>
            <button onclick="deleteProduct(${p.id})">Eliminar</button>
          `;
          productList.appendChild(card);
        });
      });
  }

  // === Enviar formulario PRODUCTO ===
  formProducto.onsubmit = function (e) {
    e.preventDefault(); // evito recargar página
    const nombre = formProducto.querySelector('[name="nombreProducto"]').value;
    const descripcion = formProducto.querySelector('[name="descripcionProducto"]').value;
    const precio = parseFloat(formProducto.querySelector('[name="precioProducto"]').value);

    const data = { nombre, descripcion, precio };

    if (editIdProducto) {
      // === Actualizar producto existente ===
      fetch(`${apiProductos}/${editIdProducto}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(() => {
        formProducto.reset();
        editIdProducto = null;
        loadProducts();
      });
    } else {
      // === Crear nuevo producto ===
      fetch(apiProductos, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(() => {
        formProducto.reset();
        loadProducts();
      });
    }
  };

  // === Editar producto ===
  window.editProduct = function (id, nombre, descripcion, precio) {
    formProducto.querySelector('[name="nombreProducto"]').value = nombre;
    formProducto.querySelector('[name="descripcionProducto"]').value = descripcion;
    formProducto.querySelector('[name="precioProducto"]').value = precio;
    editIdProducto = id;
  };

  // === Eliminar producto ===
  window.deleteProduct = function (id) {
    if (confirm('¿Seguro que quieres eliminar este producto?')) {
      fetch(`${apiProductos}/${id}`, { method: 'DELETE' })
        .then(() => loadProducts());
    }
  };

});
