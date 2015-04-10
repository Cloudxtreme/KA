/* This will soon use some kind of Transpiler-packager-creator-inator that I will make sometime */

/* jslint esnext: true */
/* jslint evil: true */
var fs = require('fs');
var path = require('path');
var beautifier = require('js-beautify').html_beautify;
const config = {
	defaultSource: '/views/',
	defaultDest: '/xml/'
};

var source = process.argv[2] || config.defaultSource;
var dest = process.argv[3] || config.defaultDest;

function attack() {
	var aPath = path.join(process.cwd(), source),
		pathInfo = fs.statSync(aPath);
	if (pathInfo.isDirectory()) {
		return fs.readdirSync(aPath).map(function(aLoc) {
			return path.join(aPath, aLoc);
		}).forEach(transpile);
	}
	return transpile(path);
}

function transpile(loc) {
	if (fs.statSync(loc).isDirectory()) return;
	var file = fs.readFileSync(loc).toString(),
		xml = '';
	try {
		xml = generateXML(JSON.parse(file));
	} catch (er) {
		console.error('Your JSON map seems to be invalid, error thrown at eval:', er);
		process.exit();
	}
	fs.writeFile(file = path.join(process.cwd(), dest, path.parse(loc).base).replace('.json', ''), xml, function(err) {
		if (err) throw err;
		console.log(path + ' transpiled to ' + file);
	});
}

function generateXML(tree) {
	"use strict";

	function generate(tree, wrapAsChilds) {
		var doc = "";
		Object.keys(tree).forEach(function(key) {
			var arr = key.split("#");
			var node = `<object class="Gtk${arr[0]}" ${arr[1]?'id="'+arr[1]+'"':''}>`;
			Object.keys(tree[key]).forEach(function(prop) {
				if (prop === "children" || prop === "signals") return;
				var propNode = `<property name="${prop}">${tree[key][prop]}</property>`;
				node += propNode;
			});
			if (tree[key].signals) {
				Object.keys(tree[key].signals).forEach(function(signal) {
					var sig = `<signal name="${signal}" handler="${tree[key].signals[signal]}"/>`;
					node += sig + "\n";
				});
			}
			if (tree[key].children) {
				var childTree = generate(tree[key].children, true);
				node += childTree;
			}
			node += '</object>';
			if (wrapAsChilds) doc += `<child>${node}</child>`;
			else doc += node;
		});
		return doc;
	}

	var ret = `<?xml version="1.0" encoding="UTF-8"?><interface>${generate(tree)}</interface>`;
	return beautifier(ret);
}

attack();

fs.watch(path.join(process.cwd(), source), function (event, filename) {
	console.log(`${event} triggered by ${filename}`);
	attack();
});
