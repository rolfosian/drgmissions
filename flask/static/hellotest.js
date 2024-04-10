// function dummy() {
//     // do something
// }

// // document.addEventListener('DOMContentLoaded', function() {
// //     html = '<img src="/static/img/image.png">'
// //     document.getElementById('test').innerHTML = html
// //     dummy();
// // });

// async function topz() {
//     return 'face'
// }

// async function bottomz() {
//     let promises = [facez(), facez(), topz(), topz(),facez(), facez(), topz(), topz(),facez(), facez(), topz(), topz(),facez(), facez(), topz(), topz(), sidez()]
//     return Promise.all(promises)
// }

// async function facez() {
//     // console.log('top')
//     return 'top'
// }

// async function sidez() {
//     return 'side'
// }

// async function asyncfunction1() {
//     let promises = [bottomz(), bottomz(), bottomz()]
//     return Promise.all(promises)
// }

// async function asyncfunction() {
//     let promises = [
//         asyncfunction1(),
//         asyncfunction1(),
//         asyncfunction1(),
//         asyncfunction1(),
//         asyncfunction1()
//     ]
//     results = await Promise.all(promises)
//     return results 
// }

// // results = asyncfunction()
// // console.log(results)
// // for (result of results) {
// //     console.log(typeof result)
// // }

// // document.addEventListener('DOMContentLoaded', function() {
// //     html = '<img src="/static/img/image.png">'
// //     document.getElementById('test').innerHTML = html
// //     dummy();
// // });

// document.addEventListener('DOMContentLoaded', async function() {
//     results = await asyncfunction()
//     console.log(results)
//     console.log('-------------------------------------------')
//     for (result of results) {
//         console.log(result)
//         console.log('-------------------------------------------')
//         for (result_ of result) {
//             console.log(result_)
//         }
        
//     }
// });

var arr = [1, 2, 3];
var obj = { key: 'value' };

console.log(Array.isArray(arr)); // true
console.log(Array.isArray(obj)); // false