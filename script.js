/*
let request = new XMLHttpRequest();
request.open("GET", "http://127.0.0.1:5000/events/0");
request.send();
request.onload = () => {
	if (request.status == 200) {
		var first = JSON.parse(request.response);
		console.log(first.dungeon);
		dungeon_ = document.getElementById("dung");
		dungeon_.innerHTML = first.dungeon;
		starter_ = document.getElementById("start");
		starter_.innerHTML = first.starter;
		info_ = document.getElementById("inf");
		info_.innerHTML = first.info;
		console.log(first)
	} else {
		console.log('API offline');
	}
}
*/