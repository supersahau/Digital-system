// pages/exception.js
import * as echarts from '../../ec-canvas/echarts';

const app = getApp();
var tmp = 1;
var mychart;

function initChart(canvas, width, height) {
  mychart = echarts.init(canvas, null, {
    width: width,
    height: height
  });
  canvas.setChart(mychart);
  var option = {
    backgroundColor: "#ffffff",
    color: ["#37A2DA", "#32C5E9", "#67E0E3"],
    series: [{
      name: '业务指标',
      type: 'gauge',
      radius: '98%',
      silent: true,
      detail: {
        formatter: '{value}%',
        fontSize: 22,
      },
      title: {
        fontSize: 18,
        fontWeight: 'bold',
        fontStyle: 'italic'
      },
      axisLine: {
        show: true,
        lineStyle: {
          width: 30,
          shadowBlur: 0,
          color: [
            [0.3, '#67e0e3'],
            [0.7, '#37a2da'],
            [1, '#fd666d']
          ]
        }
      },
      axisLabel: {
        fontSize: 8
      },
      data: [{
        value: ((1 - app.globalData.jsonlist.sim) * 100).toFixed(2),
        name: '异常值',
      }]
    }]
  };

  mychart.setOption(option, true);
  return mychart;
}

Page({

  /**
   * 页面的初始数据
   */
  data: {
    ec: {
      onInit: initChart
    },
    symsim:'',
    contentlist:'',
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    var that = this;
    console.log(((1 - app.globalData.jsonlist.sim) * 100).toFixed(2));
    that.setData({
      symsim: app.globalData.jsonlist.symsim,
      contentlist: app.globalData.jsonlist.comment,
    })
  },

  /**
   * 生命周期函数--监听页面初次渲染完成
   */
  onReady: function () {
  
  },

  /**
   * 生命周期函数--监听页面显示
   */
  onShow: function () {
    var that = this
    that.setData({
      symsim: app.globalData.jsonlist.symsim,
      contentlist: app.globalData.jsonlist.comment,
    })
    if (tmp > 1) {
      var option = {
    backgroundColor: "#ffffff",
    color: ["#37A2DA", "#32C5E9", "#67E0E3"],
    series: [{
      name: '业务指标',
      type: 'gauge',
      radius: '98%',
      silent: true,
      detail: {
        formatter: '{value}%',
        fontSize: 22,
      },
      title: {
        fontSize: 18,
        fontWeight: 'bold',
        fontStyle: 'italic'
      },
      axisLine: {
        show: true,
        lineStyle: {
          width: 30,
          shadowBlur: 0,
          color: [
            [0.3, '#67e0e3'],
            [0.7, '#37a2da'],
            [1, '#fd666d']
          ]
        }
      },
      axisLabel: {
        fontSize: 8
      },
      data: [{
        value: ((1 - app.globalData.jsonlist.sim) * 100).toFixed(2),
        name: '异常值',
      }]
    }]
  };
      that.setData({
        ec: {
          onInit: mychart.setOption(option, true)
        }
      })
    }
    else { tmp = tmp + 1 }
  },

  /**
   * 生命周期函数--监听页面隐藏
   */
  onHide: function () {
  
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function () {
  
  },

  /**
   * 页面相关事件处理函数--监听用户下拉动作
   */
  onPullDownRefresh: function () {
  
  },

  /**
   * 页面上拉触底事件的处理函数
   */
  onReachBottom: function () {
  
  },

  /**
   * 用户点击右上角分享
   */
  onShareAppMessage: function () {
  
  }
})