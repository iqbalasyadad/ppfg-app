import React from "react";
import axios from 'axios'
import FileSaver from 'file-saver';
import Plot from 'react-plotly.js';
import './CombinedPPPTabContent.css'

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

function ColorLuminance(hex, lum) {
    // validate hex string
    hex = String(hex).replace(/[^0-9a-f]/gi, '');
    if (hex.length < 6) {
      hex = hex[0]+hex[0]+hex[1]+hex[1]+hex[2]+hex[2];
    }
    lum = lum || 0;
  
    // convert to decimal and change luminosity
    var rgb = "#", c, i;
    for (i = 0; i < 3; i++) {
      c = parseInt(hex.substr(i*2,2), 16);
      c = Math.round(Math.min(Math.max(0, c + (c * lum)), 255)).toString(16);
      rgb += ("00"+c).substr(c.length);
    }
  
    return rgb;
  }

class CombinedPPPlotPlotly extends React.Component {
    constructor(props){
        super(props)
    }
    render() {
        let traces = []
        for (let i=0;i <this.props.selectedWellsPMPPP.length; i++) {
            const trace_PP = {
                x: this.props.selectedWellsPMPPP[i].PP.PP_SG,
                y: this.props.selectedWellsPMPPP[i].PP.PP_TVDSS_M,
                type: 'scatter',
                mode: 'lines',
                marker: {color: this.props.wellColors[i]},
                name: 'PP ' + this.props.selectedWellsPMPPP[i].SHORT_NAME
            }
            traces.push(trace_PP)
        }
        
        // add MW
        for (let i=0;i <this.props.selectedWellsPMPPP.length; i++) {
            const trace_MW = {
                x: this.props.selectedWellsPMPPP[i].MW.MW_SG,
                y: this.props.selectedWellsPMPPP[i].MW.MW_TVDSS_M,
                type: 'scatter',
                mode: 'lines',
                marker: {color: this.props.wellColors[i]},
                name: 'MW ' + this.props.selectedWellsPMPPP[i].SHORT_NAME
            }
            traces.push(trace_MW)
        }

        // add PT
        for (let i=0;i <this.props.selectedWellsPMPPP.length; i++) {
            const trace_PT = {
                x: this.props.selectedWellsPMPPP[i].PT.PT_SG,
                y: this.props.selectedWellsPMPPP[i].PT.PT_TVDSS_M,
                type: 'scatter',
                mode: 'markers',
                marker: {color: this.props.wellColors[i], line:{color:'black', width:1}},
                name: 'PT ' + this.props.selectedWellsPMPPP[i].SHORT_NAME
            }
            traces.push(trace_PT)
        }
        // add event
        for (let i=0;i <this.props.selectedWellsPMPPP.length; i++) {
            const trace_event = {
                x: this.props.selectedWellsPMPPP[i].EVENT.EVENT_PLOT_SG,
                y: this.props.selectedWellsPMPPP[i].EVENT.EVENT_PLOT_TVDSS_M,
                text: this.props.selectedWellsPMPPP[i].EVENT.EVENT_DETAIL,
                type: 'scatter',
                mode: 'markers',
                textposition: 'middle right',
                marker: {color: this.props.wellColors[i], symbol: 'star', size:9,
                            line: {color: 'black', width:1}
                        },
                name: 'event ' + this.props.selectedWellsPMPPP[i].SHORT_NAME
            }
            traces.push(trace_event)
        }
        

        return (
          <Plot
            data={traces}
            layout={{ autosize:true, plot_bgcolor:"#FFF3DF", paper_bgcolor:"#FFF3DF", dragmode: 'pan', showlegend: true, font: {size: 10},
                legend:{ x: 1.3, xanchor: 'right', y: 1, borderwidth:1},
                margin:{l:50, r:15, b:50, t:30, pad:5},
                title: {text: "Combined", font: {size:10}},
                xaxis:{title:'SG', range:[0.5,3], showline:true, dtick:0.5, tickwidth:1.5, ticks:'outside', tickcolor:'black', gridwidth:2, mirror:'ticks',
                  minor:{dtick:0.1, tickcolor:'black', tickwidth:1, showgrid:true, gridwidth:1, gridcolor:"#E1E1E1"}}, 
                yaxis:{title:'TVDSS (m)', showgrid:true, tickwidth:1.5, range: [4000, 0], showline:true, ticks:'outside', tickcolor:'black', gridwidth:2, mirror:'ticks',
                  minor:{dtick:100, tickcolor:'black', tickwidth:1, showgrid:true, gridwidth:1,gridcolor:"#E1E1E1"}} }}
            config={{ scrollZoom:true }}
            useResizeHandler={true}
            style={{height: '100%', width: '100%'}}
          />
        );
      }
}

class CombinedPPAnmPlotPlotly extends React.Component {
    constructor(props){
        super(props)
      }
    render() {
        let traces = []

        if (!isEmpty(this.props.pMarker)) {
            const trace_marker = {
                x: this.props.pMarker.MARKER_PLOT_X,
                y: this.props.pMarker.MARKER_TVDSS_M,
                text: this.props.pMarker.MARKER_NAME,
                type: 'scatter',
                mode: 'markers+text',
                textposition: 'middle right',
                marker: {color: 'black', symbol: 'triangle-left'},
                name: 'marker'
            }
            traces.push(trace_marker)
        }

        if (!isEmpty(this.props.combinedPPPAnm)) {
            for (var id in this.props.combinedPPPAnm) {
                if (this.props.combinedPPPAnm.hasOwnProperty(id)) {
                    const trace_PP = {
                        x: this.props.combinedPPPAnm[id].PP_SG,
                        y: this.props.combinedPPPAnm[id].PP_TVDSS_M,
                        type: 'scatter',
                        mode: 'lines',
                        marker: {color: this.props.wellColors[id]},
                        name: 'PP ' + this.props.combinedPPPAnm[id].SHORT_NAME
                    }
                    traces.push(trace_PP)
                }
            }
            for (let id in this.props.combinedPPPAnm) {
                if (this.props.combinedPPPAnm.hasOwnProperty(id)) {
                    const trace_PT = {
                        x: this.props.combinedPPPAnm[id].PT_SG,
                        y: this.props.combinedPPPAnm[id].PT_TVDSS_M,
                        type: 'scatter',
                        mode: 'markers',
                        marker: {color: this.props.wellColors[id], symbol: 'circle',
                            line: {color: 'black', width:1}
                        },
                        name: 'PT ' + this.props.combinedPPPAnm[id].SHORT_NAME
                    }
                    traces.push(trace_PT)
                }
            }
            for (let id in this.props.combinedPPPAnm) {
                if (this.props.combinedPPPAnm.hasOwnProperty(id)) {
                    const trace_event = {
                        x: this.props.combinedPPPAnm[id].EVENT_PLOT_SG,
                        y: this.props.combinedPPPAnm[id].EVENT_PLOT_TVDSS_M,
                        text: this.props.combinedPPPAnm[id].EVENT_DETAIL,
                        type: 'scatter',
                        mode: 'markers',
                        textposition: 'middle right',
                        marker: {color: this.props.wellColors[id], symbol: 'star', size:9,
                                    line: {color: 'black', width:1}
                                },
                        name: 'event ' + this.props.combinedPPPAnm[id].SHORT_NAME
                    }
                    traces.push(trace_event)
                }
            }
        }

        return (
          <Plot
            data={traces}
            layout={{ autosize:true, plot_bgcolor:"#FFF3DF", paper_bgcolor:"#FFF3DF", dragmode: 'pan', showlegend: true, font: {size: 10},
                legend:{ x: 1.3, xanchor: 'right', y: 1, borderwidth:1},
                margin:{l:50, r:15, b:50, t:30, pad:5},
                title: {text: "Anamorph to " + this.props.pWell, font: {size:10}},
                xaxis:{title:{text: 'SG', font:{size:10}}, range:[0.5,3], showline:true, dtick:0.5, tickwidth:1.5, ticks:'outside', tickcolor:'black', gridwidth:2, mirror:'ticks',
                  minor:{dtick:0.1, tickcolor:'black', tickwidth:1, showgrid:true, gridwidth:1, gridcolor:"#E1E1E1"}}, 
                yaxis:{title:{text: 'TVDSS (m)', font:{size:10}}, showgrid:true, tickwidth:1.5, range: [4000, 0], showline:true, ticks:'outside', tickcolor:'black', gridwidth:2, mirror:'ticks',
                  minor:{dtick:100, tickcolor:'black', tickwidth:1, showgrid:true, gridwidth:1,gridcolor:"#E1E1E1"}}}}
            config={{ scrollZoom:true }}
            useResizeHandler={true}
            style={{height: '100%', width: '100%'}}
          />
        );
      }
}

class CombinedPPPlotDesc extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            combinedPPDownloadExcelBtnDisabled: false,
            combinedPPDownloadZipBtnDisabled: false,
        }
    }
    async downloadPPPCombinedCommon() {
        try {
            this.setState({combinedPPDownloadExcelBtnDisabled: true})
            const dataParam = {
                wellNames: this.props.selectedSummWells
            }
            const resp = await axios({
                method: 'POST',
                url: 'http://localhost:5000/downloadpppcombinedcommonexcel',
                data: dataParam,
                responseType: 'blob'
            });
            FileSaver.saveAs(resp.data, resp.headers['x-filename']);
            this.setState({combinedPPDownloadExcelBtnDisabled: false})
    
        } catch (err) {
            console.error(err);
        } 
    }
    async downloadPPPCombinedCommonZip() {
        try {
            this.setState({combinedPPDownloadZipBtnDisabled: true})
            const dataParam = {
                wellNames: this.props.selectedSummWells,
            }
            const resp = await axios({
                method: 'POST',
                url: 'http://localhost:5000/downloadpppcombinedcommonzip',
                data: dataParam,
                responseType: 'blob'
            });
            FileSaver.saveAs(resp.data, resp.headers['x-filename']);
            this.setState({combinedPPDownloadZipBtnDisabled: false})
    
        } catch (err) {
            console.error(err);
        } 
    }

    render() {

        return(
            <table className="combinedpp-desc-table-table">
                <tbody>
                    <tr className="combinedpp-desc-table-tr">
                        <td className="combinedpp-desc-table-td">
                            <button className='combinedpp-download-btn' 
                                onClick={()=>{this.downloadPPPCombinedCommon()}} 
                                disabled={this.state.combinedPPDownloadExcelBtnDisabled}
                                >Download as excel</button>
                        </td>
                    </tr>
                    <tr className="combinedpp-desc-table-tr">
                        <td className="combinedpp-desc-table-td">
                            <button className='combinedpp-download-btn' 
                                onClick={()=>{this.downloadPPPCombinedCommonZip()}} 
                                disabled={this.state.combinedPPDownloadZipBtnDisabled}
                                >Download as zip</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        );
    }
}

class CombinedPPAnmPlotDesc extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            combinedPPAnmDownloadExcelBtnDisabled: false,
            combinedPPAnmDownloadZipBtnDisabled: false
        }
    }
    async downloadPPPCombinedAnm() {
        try {
            this.setState({combinedPPAnmDownloadExcelBtnDisabled: true})
            const dataParam = {
                pWellName: this.props.pWell,
                wellNames: this.props.selectedSummWells
            }
            const resp = await axios({
                method: 'POST',
                url: 'http://localhost:5000/downloadpppcombinedanmexcel',
                data: dataParam,
                responseType: 'blob'
            });
            FileSaver.saveAs(resp.data, resp.headers['x-filename']);
            this.setState({combinedPPAnmDownloadExcelBtnDisabled: false})
        } catch (err) {
            console.error(err);
        } 
    }
    async downloadPPPCombinedAnmZip() {
        try {
            this.setState({combinedPPAnmDownloadZipBtnDisabled: true})
            const dataParam = {
                pWellName: this.props.pWell,
                wellNames: this.props.selectedSummWells
            }
            const resp = await axios({
                method: 'POST',
                url: 'http://localhost:5000/downloadpppcombinedanmzip',
                data: dataParam,
                responseType: 'blob'
            });
            FileSaver.saveAs(resp.data, resp.headers['x-filename']);
            this.setState({combinedPPAnmDownloadZipBtnDisabled: false})
    
        } catch (err) {
            console.error(err);
        } 
    }

    render() {

        return(
            <table className="combinedpp-desc-table-table">
                <tbody>
                    <tr className="combinedpp-desc-table-tr">
                        <td className="combinedpp-desc-table-td">
                        <button className='combinedpp-download-btn' 
                            onClick={()=>{ this.downloadPPPCombinedAnm() }}
                            disabled={this.state.combinedPPAnmDownloadExcelBtnDisabled}
                            >Download as excel
                        </button>
                        </td>
                    </tr>
                    <tr className="combinedpp-desc-table-tr">
                        <td className="combinedpp-desc-table-td">
                        <button className='combinedpp-download-btn' 
                            onClick={()=>{ this.downloadPPPCombinedAnmZip() }}
                            disabled={this.state.combinedPPAnmDownloadZipBtnDisabled}
                            >Download as zip
                        </button>
                        </td>
                    </tr>
                </tbody>
            </table>
        );
    }
}

class CombinedPPPTabContent extends React.Component{

    constructor(props){
        super(props)
    }

    render() {
        
        if (this.props.selectedSummWells.length===0) {
            return (
                <></>
            );
        } else {
            let wellColors = []
            for (var i=0; i<this.props.selectedSummWells.length; i++) {
                const randomColor = Math.floor(Math.random()*16777215).toString(16);
                const randColorUpdate = ColorLuminance(randomColor, 0)
                wellColors.push(randColorUpdate)
            }

            if (this.props.combinedMode==="well") {
                return(
                    <>
                        <div className='combinedpp-plot-container'>
                            <div className='combinedpp-plot-plotly-container'>
                                <CombinedPPPlotPlotly 
                                    selectedWellsPMPPP={this.props.selectedWellsPMPPP} 
                                    wellColors={wellColors}
                                />
                            </div>
                            <div className='combinedpp-plot-desc-container'>
                                <CombinedPPPlotDesc 
                                    selectedSummWells={this.props.selectedSummWells}
                                />
                            </div>
                        </div>
                        <div className='combinedpp-plot-container'>
                            <div className='combinedpp-plot-plotly-container'>
                                <CombinedPPAnmPlotPlotly 
                                    pWell={this.props.pWell} 
                                    pMarker={this.props.pMarker} 
                                    combinedPPPAnm={this.props.combinedPPPAnm}
                                    wellColors={wellColors}
                                />
                            </div>
                            <div className='combinedpp-plot-desc-container'>
                                <CombinedPPAnmPlotDesc 
                                    pWell={this.props.pWell}
                                    selectedSummWells={this.props.selectedSummWells}
                                />
                            </div>
                        </div>
                    </>
                );
            }
            else if (this.props.combinedMode==="point") {
                return (
                    <>
                        <div className='combinedpp-plot-container'>
                            <div className='combinedpp-plot-plotly-container'>
                                <CombinedPPPlotPlotly 
                                    selectedWellsPMPPP={this.props.selectedWellsPMPPP} 
                                    wellColors={wellColors}
                                />
                            </div>
                        </div>
                    </>
                );
            } else {
                return (
                    <></>
                );
            }
        }

        

    }
}

export default CombinedPPPTabContent;