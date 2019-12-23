importScripts("math.min.js");
importScripts("utils.js");

/**
* Convert degrees to radians
* @param {number} degrees degrees
* @return {number} radians
*/
function radians(degrees) {
    return degrees * math.pi / 180;
}

/**
* Convert radians to degrees
* @param {number} rad radians
* @return {number} degrees
*/
function degrees(rad) {
    return rad * 180 / math.pi;
}

/**
* Retrieve a row from a matrix
* @param {Matrix | Array} matrix
* @param {number} index    Zero based row index
* @return {Matrix | Array} Returns the row as a vector
* @source https://github.com/josdejong/mathjs/issues/230
*/
function row(matrix, index) {
    var rows = math.size(matrix).valueOf()[1];
    return math.flatten(math.subset(matrix, math.index(index, math.range(0, rows))));
}

/**
* Transform vectors on the unit sphere to radec
* @param {number} telra Right ascension for telescope center
* @param {number} teldec  Declination for telescope center
* @param {Matrix | Array} v A matrix containing 3 dimensional
*                           vectors on the unit sphere to be transformed
* @return {Matrix | Array} A matrix containing radec vectors in radians
* @source desimodel.geometry.xy2radec
*/
function xyz2radec(telra, teldec, v) {
    // Clockwise rotation around y axis by declination of the tile center
    var decrotate = math.zeros(3, 3);
    var teldec_rad = radians(teldec);
    decrotate = math.subset(decrotate, math.index(0, [0, 1, 2]), [math.cos(teldec_rad), 0, -math.sin(teldec_rad)]);
    decrotate = math.subset(decrotate, math.index(1, [0, 1, 2]), [0, 1, 0]);
    decrotate = math.subset(decrotate, math.index(2, [0, 1, 2]), [math.sin(teldec_rad), 0, math.cos(teldec_rad)]);

    // Counter-clockwise rotation around the z-axis by the right ascension of the tile center
    var rarotate = math.zeros(3,3);
    var telra_rad = radians(telra);
    rarotate = math.subset(rarotate, math.index(0, [0, 1, 2]), [math.cos(telra_rad), -math.sin(telra_rad), 0]);
    rarotate = math.subset(rarotate, math.index(1, [0, 1, 2]), [math.sin(telra_rad), math.cos(telra_rad), 0]);
    rarotate = math.subset(rarotate, math.index(2, [0, 1, 2]), [0, 0, 1]);

    var v3 = math.multiply(rarotate, math.multiply(decrotate, v));
    
    var x3 = row(v3, 0);
    var y3 = row(v3, 1);
    var z3 = row(v3, 2);

    var ra_rad = math.atan2(y3, x3);
    var dec_rad = math.add(math.multiply(-1, math.acos(z3)), math.pi/2);
    
    return [ra_rad, dec_rad];
}
