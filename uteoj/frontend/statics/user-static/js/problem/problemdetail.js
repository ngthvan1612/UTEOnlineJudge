$(function () {
    $('[data-toggle="popover"]').popover({html:true})
})
document.getElementById('statement').innerHTML = marked(document.getElementById('statement').innerHTML);
document.getElementById('input').innerHTML = marked(document.getElementById('input').innerHTML);
document.getElementById('constraints').innerHTML = marked(document.getElementById('constraints').innerHTML);
document.getElementById('output').innerHTML = marked(document.getElementById('output').innerHTML);


let myChart = document.getElementById('myChart').getContext('2d');

//Get Total Submission
let totalSubmission = Number(document.getElementById('total').textContent);

if (totalSubmission !== 0){
    // Global Options
    let massPopChart = new Chart(myChart, {
        type:'pie', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
        data:{
            labels:['AC','WA','RTE','MLE','TLE','CE'],
            datasets:[{
                data:[
                    Number(document.getElementById('ac').textContent),
                    Number(document.getElementById('wa').textContent),
                    Number(document.getElementById('rte').textContent),
                    Number(document.getElementById('mle').textContent),
                    Number(document.getElementById('tle').textContent),
                    Number(document.getElementById('ce').textContent)
                ],
                backgroundColor:[
                    'rgb(27, 209, 117)',
                    'rgb(255, 69, 22)',
                    'rgb(255, 106, 4)',
                    'rgb(49, 154, 255)',
                    'rgb(255, 161, 0)',
                    'rgb(140, 145, 157)'
                ],
                borderWidth:2,
                borderColor:'#000',
                hoverBorderWidth: 4,
                hoverBorderColor: '#000'
            }]
            },
            options:{
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            filter: (legendItem, data) => data.datasets[0].data[legendItem.index] != 0,
                            color: 'rgb(255, 99, 132)'
                        }
                    },
                    datalabels:{
                        color: '#000',
                        labels: {
                            title: {
                                font: {
                                    weight: 'bold'
                                }
                            }
                        }
                    }
                },
                layout:{
                    padding:{
                    left:50,
                    right:0,
                    bottom:0,
                    top:0
                    }
                },
                tooltips:{
                    enabled:true
                },
                reponsive: true
        }
    });
}
else{
    console.log(totalSubmission)
    let massPoppChart = new Chart(myChart, {
        type:'pie', // bar, horizontalBar, pie, line, doughnut, radar, polarArea
        data:{
            labels:['No submission for this problem'],
            datasets:[{
                data: [1],
                backgroundColor:[
                    'rgb(255,255,255)'
                ],
                borderWidth:2,
                borderColor:'#000',
                hoverBorderWidth: 4,
                hoverBorderColor: '#fff'
            }]
        },
        options:{
            plugins: {
                legend:     {
                    display: true,
                }
            },
            layout:{
                padding:{
                    left:50,
                    right:0,
                    bottom:0,
                    top:0
                }
            },
            tooltips:{
                enabled:true
            },
            reponsive: true
        }
    });
}