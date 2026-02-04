#!/usr/bin/env node

import fs from 'fs';

main();

function main() {
    let str = fs.readFileSync(process.argv[2], 'utf-8');
    let obj = JSON.parse(str);
    console.log(sum(obj));
}

function sum(obj) {
    switch (typeof obj) {
        case 'number': return obj;
        case 'object': {
            let values = Object.values(obj);
            if (!Array.isArray(obj) && values.includes("red")) {
                return 0;
            }
            return values.map(sum).reduce((acc, v) => acc + v, 0);
        }
    }
    return 0;
}
