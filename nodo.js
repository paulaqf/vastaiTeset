if (msg.payload) {
    const data = [];

    // Function to determine the type of data
    const determineType = (obj) => {
        const types = ["discos-duros", "procesadores", "tarjetas-graficas", "placas-base", "memorias-ram", "refrigeracion-liquida", "maquinas"];
        for (let type of types) {
            if (obj.hasOwnProperty(type)) {
                return type;
            }
        }
        return 'unknown';
    }

    // Since payload is an object
    const type = determineType(msg.payload);

    // If type is 'maquinas', send to output 1
    if (type === 'maquinas') {
        data[0] = { payload: msg.payload };
    } 
    // If type is not 'maquinas', send to output 2
    else {
        data[1] = { payload: msg.payload };
    }

    return data;
} else {
    return [null, null];
}