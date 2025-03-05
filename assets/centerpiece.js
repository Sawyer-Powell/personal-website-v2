import * as THREE from 'three';

function generateNormal(mean = 0, stdDev = 1) {
  // Box-Muller transform
  const u1 = Math.random();
  const u2 = Math.random();
  
  // Create two independent standard normal random variables
  const z0 = Math.sqrt(-2.0 * Math.log(u1)) * Math.cos(2.0 * Math.PI * u2);
  
  // Transform to desired mean and standard deviation
  return z0 * stdDev + mean;
}

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera( 60, 1, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer(
	{
		alpha: true,
		antialias: true,
	}
);

renderer.setPixelRatio(1.);

const mainEl = document.getElementById('centerpiece')

function getDimensions() {
	let res = Math.min(mainEl.clientWidth, 800)
	return [res, res]
}

renderer.setSize( getDimensions()[0], getDimensions()[1]);

renderer.setAnimationLoop( animate );
mainEl.appendChild( renderer.domElement );

const geometry = new THREE.SphereGeometry( 0.015 );

var spheres = new THREE.Group();

function randColor() {
	return new THREE.Color(0xfb4934).lerp(new THREE.Color(0xb8bb26), Math.random());
}

function addLine(spheres) {
	let first = THREE.MathUtils.randInt(0, spheres.children.length - 1);
	let second = THREE.MathUtils.randInt(0, spheres.children.length - 1);

	let first_child = spheres.children[first]
	let second_child = spheres.children[second]

	const color = randColor();
	const material = new THREE.LineBasicMaterial({color: color});
	const geometry = new THREE.BufferGeometry().setFromPoints([first_child.position, second_child.position]);
	const line = new THREE.Line(geometry, material);
	spheres.add(line);
}

for (var i = 0; i < 1000; i++) {
	const color = randColor();
	const material = new THREE.MeshBasicMaterial( { color: color } );
	let sphere = new THREE.Mesh( geometry, material);

	let vec = new THREE.Vector3(generateNormal(), generateNormal(), generateNormal())
	vec = vec.normalize().multiplyScalar(2.)

	sphere.position.x = vec.x
	sphere.position.y = vec.y
	sphere.position.z = vec.z

	spheres.add(sphere)
}

for (var i = 0; i < 40; i++) {
	addLine(spheres)
}

scene.add(spheres)

camera.position.z = 5;
function waitForNextFrame() {
    return new Promise(resolve => {
        requestAnimationFrame(resolve);
    });
}
async function animate() {
	await waitForNextFrame();
	spheres.rotation.y += 0.0003337;
	spheres.rotation.x += 0.000692;
	spheres.rotation.z += 0.0004;

	renderer.setSize( getDimensions()[0], getDimensions()[1] );
	renderer.render( scene, camera );
}
