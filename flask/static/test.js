function compareFuncs(funcsAndParams, iterations) {
    function measurePerformance(func, params) {
        let start;
        let end;
        if (Array.isArray(params)) {
            start = performance.now();
            func(...params);
            end = performance.now();
        } else {
            start = performance.now()
            func(params);
            end = performance.now()
        }
        
        const timeTaken = end - start;
        return timeTaken
    }
    function findMedian(arr) {
        arr.sort((a, b) => a - b);
        const middleIndex = Math.floor(arr.length / 2);
        if (arr.length % 2 === 0) {
            return (arr[middleIndex - 1] + arr[middleIndex]) / 2;
        } else {
            return arr[middleIndex];
        }
    }

    let funcs = []
    funcsAndParams.forEach(funcAndParams => {
        funcs.push(funcAndParams[0])
    })
    let measures_ = {};

    funcs.forEach(func => {
        measures_[func.name] = [];
    });

    let count = 0;

    for (let i = 0; i < iterations; i++) {
        funcs.forEach(func => {
            const result = measurePerformance(func, funcsAndParams[funcs.indexOf(func)][1]);
            if (result > 0) {
                measures_[func.name].push(result);
                count += 1;
                if (count % 100 === 0) {
                    console.log(count);
                }
            }
        });
    }

    funcMedians = [];
    funcs.forEach(func => {
        let median = findMedian(measures_[func.name]);
        console.log(`${func.name} median: ${findMedian(measures_[func.name])}`);
        funcMedians.push(median)
    });

    if (funcs.length >= 3) {
        let fastest = Math.min(...funcMedians)
        let fastestFunc = funcs[funcMedians.indexOf(fastest)]
        console.log(`Fastest function was ${fastestFunc.name} at ${fastest}`)
    }

}

function dummy(param1, param2) {
    console.log(param1, param2)
}

function dummy1(param1, param2) {
    console.log(param1, param2)
}

function dummy2(param1, param2) {
    console.log(param1, param2)
}

function dummy3(param1) {
    console.log(param1)
}

function main (){
    let funcsAndParams = [
        [dummy, ['foo', 'bar']], 
        [dummy1, ['bar', 'foo']], 
        [dummy2, ['hello', 'world']],
        [dummy3, 'world hello']
        ];
    compareFuncs(funcsAndParams, 500)
}
// main()


// let funcsAndParams = [
//     [ []],
//     [ []]
// ];

// compareFuncs(funcsAndParams, 500)

// localStorages = {
//     'seasonSelected' : 's5'
// }

// document.addEventListener('DOMContentLoaded', () => {
//     let seasonBoxValues = {
//         's0' : 'No Season',
//         's1': 'Season 1',
//         's2': 'Season 2', 
//         's3': 'Season 3', 
//         's4': 'Season 4', 
//         's5': 'Season 5'
//     };
//     let seasonBox = document.getElementById('season')
//     for (let season in seasonBoxValues) {
//         let option = document.createElement('option');
//         option.value = season;
//         option.textContent = seasonBoxValues[season];
//         seasonBox.appendChild(option);
//         if (season === localStorages['seasonSelected']) {
//             seasonBox.value = season
//         }
//     }
// })