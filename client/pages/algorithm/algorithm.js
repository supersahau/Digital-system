import * as echarts from '../../ec-canvas/echarts';

const app = getApp();

function initChart(canvas, width, height) {
  const chart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(chart);

  var option = {
    color: ["#37A2DA", "#32C5E9", "#67E0E3", "#91F2DE", "#FFDB5C", "#FF9F7F"],
    title: {
      text: '文档指纹算法框图'
    },
    tooltip: {},
    animationDurationUpdate: 1500,
    animationEasingUpdate: 'quinticInOut',
    series: [
      {
        type: 'graph',
        layout: 'none',
        symbolSize: 50,
        roam: true,
        label: {
          normal: {
            show: true
          }
        },
        // edgeSymbol: ['circle', 'arrow'],
        // edgeSymbolSize: [4, 10],
        edgeLabel: {
          normal: {
            textStyle: {
              fontSize: 20
            }
          }
        },
        data: [{
          name: '停用词',
          x:  300,
          y: 150,
          itemStyle: {
            color: '#37A2DA'
          }
        }, {
          name: '实词',
          x: 800,
          y: 150,
          itemStyle: {
            color: '#32C5E9'
          }
        }, {
          name: '原文档',
          x: 550,
          y: 0,
          itemStyle: {
            color: '#9FE6B8'
          }
        }, {
          name: 'LDA',
          x: 300,
          y: 300,
          itemStyle: {
            color: '#FF9F7F'
          }},{
          name: '同义词林',
          x: 800,
          y: 300,
          itemStyle: {
            color: '#FF9F7F'
          }},{
          name: 'GloVe+/TFIDF',
          x: 650,
          y: 300,
          itemStyle: {
            color: '#FF9F7F'
          }},{
            name: '自动编码器',
            x: 550,
            y: 450,
            itemStyle: {
              color: '#37A2DA'
            }
          },{
            name: '文档指纹',
            x: 550,
            y: 600,
            itemStyle: {
              color: '#9FE6B8'
            }
          }
        ],
        // links: [],
        links: [/*{
          source: 0,
          target: 1,
          symbolSize: [5, 20],
          label: {
            normal: {
              show: true
            }
          },
          lineStyle: {
            normal: {
              width: 4,
              curveness: 0.2
            }
          }
        }, 
        {
          source: '停用词',
          target: 'LDA',
          label: {
            normal: {
              show: false
            }
          },
          lineStyle: {
            normal: { curveness: 0.2 }
          }
        },*/
         {
          source: '原文档',
          target: '停用词'
        }, {
          source: '原文档',
          target: '实词'
        },{
          source:'停用词',
          target:'LDA'
        }, {
          source: '实词',
          target: '同义词林'
        }, {
          source: '节点1',
          target: '节点4'
        },{
          source:'实词',
          target:'GloVe+/TFIDF'
        },{
          source:'LDA',
          target:'自动编码器'
        },{
           source:'GloVe+/TFIDF',
           target:'自动编码器'
        },{
          source:'同义词林',
          target:'自动编码器'
        },{
          source:'自动编码器',
          target:'文档指纹'
        }],
        lineStyle: {
          normal: {
            opacity: 0.9,
            width: 2,
            curveness: 0
          }
        }
      }
    ]
  };

  chart.setOption(option);
  chart.on('click',function(params){
    if(params.name === '停用词'){
      var tmp='stopword';
      var imgurl = '';
      wx.request({
        url: 'http://111.231.71.74:8888/analysis',
        data: {
          id: app.globalData.globalID,
          content: tmp,
        },
        header: {
          'content-type': 'application/json'
        },
        method: 'GET',
        success: function (res) {
          console.log('submit success');
          console.log(res.data);
          imgurl = res.data;
          wx.navigateTo({
            url: '../../pages/disp/disp?imgurl=' + imgurl
          })
        },
        fail: function (res) {
          console.log('submit fail');
        },
        complete: function (res) {
          console.log('submit complete');
        }
      })
    }

    if (params.name === '实词') {
      var tmp = 'realword';
      var imgurl = '';
      wx.request({
        url: 'http://111.231.71.74:8888/analysis',
        data: {
          id: app.globalData.globalID,
          content: tmp,
        },
        header: {
          'content-type': 'application/json'
        },
        method: 'GET',
        success: function (res) {
          console.log('submit success');
          console.log(res.data);
          imgurl = res.data;
          wx.navigateTo({
            url: '../../pages/disp/disp?imgurl=' + imgurl
          })
        },
        fail: function (res) {
          console.log('submit fail');
        },
        complete: function (res) {
          console.log('submit complete');
        }
      })
    }

    if (params.name === 'LDA') {
      var tmp = 'lda';
      var imgurl = '';
      wx.request({
        url: 'http://111.231.71.74:8888/analysis',
        data: {
          id: app.globalData.globalID,
          content: tmp,
        },
        header: {
          'content-type': 'application/json'
        },
        method: 'GET',
        success: function (res) {
          console.log('submit success');
          console.log(res.data);
          imgurl = res.data;
          wx.navigateTo({
            url: '../../pages/disp/disp?imgurl=' + imgurl
          })
        },
        fail: function (res) {
          console.log('submit fail');
        },
        complete: function (res) {
          console.log('submit complete');
        }
      })
    }

    if (params.name === 'GloVe+/TFIDF') {
      var tmp = 'glove';
      var imgurl = '';
      wx.request({
        url: 'http://111.231.71.74:8888/analysis',
        data: {
          id: app.globalData.globalID,
          content: tmp,
        },
        header: {
          'content-type': 'application/json'
        },
        method: 'GET',
        success: function (res) {
          console.log('submit success');
          console.log(res.data);
          imgurl = res.data;
          wx.navigateTo({
            url: '../../pages/disp/disp?imgurl=' + imgurl
          })
        },
        fail: function (res) {
          console.log('submit fail');
        },
        complete: function (res) {
          console.log('submit complete');
        }
      })
    }

    if (params.name === '同义词林') {
      var tmp = 'sym2';
      var imgurl = '';
      wx.request({
        url: 'http://111.231.71.74:8888/analysis',
        data: {
          id: app.globalData.globalID,
          content: tmp,
        },
        header: {
          'content-type': 'application/json'
        },
        method: 'GET',
        success: function (res) {
          console.log('submit success');
          console.log(res.data);
          imgurl = res.data;
          wx.navigateTo({
            url: '../../pages/disp/disp?imgurl=' + imgurl
          })
        },
        fail: function (res) {
          console.log('submit fail');
        },
        complete: function (res) {
          console.log('submit complete');
        }
      })
    }
    
    if (params.name === '文档指纹') {
      var tmp = 'fingerprint';
      var imgurl = '';
      wx.request({
        url: 'http://111.231.71.74:8888/analysis',
        data: {
          id: app.globalData.globalID,
          content: tmp,
        },
        header: {
          'content-type': 'application/json'
        },
        method: 'GET',
        success: function (res) {
          console.log('submit success');
          console.log(res.data);
          imgurl = res.data;
          wx.navigateTo({
            url: '../../pages/disp/disp?imgurl=' + imgurl
          })
        },
        fail: function (res) {
          console.log('submit fail');
        },
        complete: function (res) {
          console.log('submit complete');
        }
      })
    }
  });
  return chart;
}

Page({
  onShareAppMessage: function (res) {
    return {
      title: 'ECharts 可以在微信小程序中使用啦！',
      path: '/pages/index/index',
      success: function () { },
      fail: function () { }
    }
  },
  data: {
    ec: {
      onInit: initChart
    }
  },

  onReady() {
  }
});
