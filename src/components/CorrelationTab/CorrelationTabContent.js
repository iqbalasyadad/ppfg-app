import React from "react";
// import axios from 'axios'
// import FileSaver from 'file-saver';
import Plot from 'react-plotly.js';
import './CorrelationTabContent.css'


function isEmpty(obj) {
    try {
        let objLength= Object.keys(obj).length;
    } catch(error) {
        return true;
    }
    return Object.keys(obj).length === 0;
}

class CorrelationPPPlotPlotly extends React.Component {
    constructor(props){
        super(props)
    }

    render() {
        let traces = []

        const layout_template = { 
            plot_bgcolor:"#FFF3DF", paper_bgcolor:"#FFF3DF", dragmode: 'pan', showlegend: true, font: {size: 10},
            legend:{ x: 1, xanchor: 'right', y: 0.98, borderwidth:1},
            margin:{l:50, r:15, b:50, t:30, pad:5}, autosize:true, 
            title: {
                text: this.props.wellPPPData.SHORT_NAME,
                font: { size: 10 }
            },
            xaxis:{title: {text: 'SG', font:{size:10}}, range:[0,5], showline:true, dtick:0.5, tickwidth:1.5, ticks:'outside', tickcolor:'black', gridwidth:2, mirror:'ticks',
            minor:{dtick:0.1, tickcolor:'black', tickwidth:1, showgrid:true, gridwidth:1, gridcolor:"#E1E1E1"}}, 
            yaxis:{title: {text: 'TVDSS (m)', font:{size:10}}, showgrid:true, tickwidth:1.5, range: [4000, 0], showline:true, ticks:'outside', tickcolor:'black', gridwidth:2, mirror:'ticks',
            minor:{dtick:100, tickcolor:'black', tickwidth:1, showgrid:true, gridwidth:1,gridcolor:"#E1E1E1"},
        }}

        if (!isEmpty(this.props.wellPPPData)) {

            const trace_RT = {
                x: this.props.wellPPPData.RT.RT_OHMM,
                y: this.props.wellPPPData.RT.RT_TVDSS_M,
                type: 'scatter',
                mode: 'lines',
                marker: {color: '#51F138'},
                name: 'RT',
                visible: 'legendonly'
            }
            traces.push(trace_RT)

            const trace_DT = {
                x: this.props.wellPPPData.DT.DT_USF,
                y: this.props.wellPPPData.DT.DT_TVDSS_M,
                type: 'scatter',
                mode: 'lines',
                marker: {color: '#DE38F1'},
                name: 'DT',
                visible: 'legendonly'
            }
            traces.push(trace_DT)

            const trace_PP = {
                x: this.props.wellPPPData.PP.PP_SG,
                y: this.props.wellPPPData.PP.PP_TVDSS_M,
                type: 'scatter',
                mode: 'lines',
                marker: {color: 'red'},
                name: 'PP'
            }
            traces.push(trace_PP)

            const trace_FG = {
                x: this.props.wellPPPData.FG.FG_SG,
                y: this.props.wellPPPData.FG.FG_TVDSS_M,
                type: 'scatter',
                mode: 'lines',
                marker: {color: 'blue'},
                name: 'FG'
            }
            traces.push(trace_FG)

            const trace_OBG = {
                x: this.props.wellPPPData.OBG.OBG_SG,
                y: this.props.wellPPPData.OBG.OBG_TVDSS_M,
                type: 'scatter',
                mode: 'lines',
                marker: {color: 'purple'},
                name: 'OBG'
            }
            traces.push(trace_OBG)

            const trace_MW = {
                x: this.props.wellPPPData.MW.MW_SG,
                y: this.props.wellPPPData.MW.MW_TVDSS_M,
                type: 'scatter',
                mode: 'lines',
                marker: {color: 'green'},
                name: 'MW'
            }
            traces.push(trace_MW)

            const trace_ECD = {
                x: this.props.wellPPPData.ECD.ECD_SG,
                y: this.props.wellPPPData.ECD.ECD_TVDSS_M,
                type: 'scatter',
                mode: 'lines',
                marker: {color: 'brown'},
                name: 'ECD'
            }
            traces.push(trace_ECD)

            const trace_LOT = {
                x: this.props.wellPPPData.LOT.LOT_SG,
                y: this.props.wellPPPData.LOT.LOT_TVDSS_M,
                type: 'scatter',
                mode: 'markers',
                marker: {color: '#7186f0', symbol: 'triangle-up', size:7, 
                            line: {color: 'black', width:1}
                        },
                name: 'LOT'
            }
            traces.push(trace_LOT)

            const trace_PT = {
                x: this.props.wellPPPData.PT.PT_SG,
                y: this.props.wellPPPData.PT.PT_TVDSS_M,
                type: 'scatter',
                mode: 'markers',
                marker: {color: '#f2bd29', symbol: 'circle',
                            line: {color: 'black', width:1}
                        },
                name: 'PT'
            }
            traces.push(trace_PT)

            const trace_marker = {
                x: this.props.wellPPPData.MARKER.MARKER_PLOT_SG,
                y: this.props.wellPPPData.MARKER.MARKER_TVDSS_M,
                text: this.props.wellPPPData.MARKER.MARKER_NAME,
                type: 'scatter',
                mode: 'markers+text',
                textposition: 'middle right',
                marker: {color: 'black', symbol: 'triangle-left'},
                name: 'marker',
                visible: 'legendonly'
            }
            traces.push(trace_marker)

            const trace_PPFG_marker = {
                x: this.props.wellPPPData.PPFG_MARKER.PPFG_MARKER_PLOT_SG,
                y: this.props.wellPPPData.PPFG_MARKER.PPFG_MARKER_TVDSS_M,
                text: this.props.wellPPPData.PPFG_MARKER.PPFG_MARKER_NAME,
                type: 'scatter',
                mode: 'markers+text',
                textposition: 'middle right',
                textfont: {
                    color: 'red'
                },
                marker: {color: 'red', symbol: 'triangle-left'},
                name: 'marker',
            }
            traces.push(trace_PPFG_marker)

            const trace_casing = {
                x: this.props.wellPPPData.CASING.CASING_PLOT_SG,
                y: this.props.wellPPPData.CASING.CASING_TVDSS_M,
                text: this.props.wellPPPData.CASING.CASING_SIZE_INCH,
                type: 'scatter',
                mode: 'markers+text',
                textposition: 'middle right',
                marker: {color: 'black', symbol: 'triangle-sw'},
                name: 'casing'
            }
            traces.push(trace_casing)

            // event losses
            let dataEventLosses = { x:[], y:[], text:[]}
            let dataEventNonLosses = { x:[], y:[], text:[]}

            var i;
            for (i=0;i<this.props.wellPPPData.EVENT.EVENT_TYPE.length;i++) {
                if (this.props.wellPPPData.EVENT.EVENT_TYPE[i]==='losses') {
                    dataEventLosses.x.push(this.props.wellPPPData.EVENT.EVENT_PLOT_SG[i])
                    dataEventLosses.y.push(this.props.wellPPPData.EVENT.EVENT_PLOT_TVDSS_M[i])
                    dataEventLosses.text.push(this.props.wellPPPData.EVENT.EVENT_DETAIL[i])
                } else {
                    dataEventNonLosses.x.push(this.props.wellPPPData.EVENT.EVENT_PLOT_SG[i])
                    dataEventNonLosses.y.push(this.props.wellPPPData.EVENT.EVENT_PLOT_TVDSS_M[i])
                    dataEventNonLosses.text.push(this.props.wellPPPData.EVENT.EVENT_DETAIL[i])
                }
            }

            const trace_event_losses = {
                x: dataEventLosses.x,
                y: dataEventLosses.y,
                text: dataEventLosses.text,
                type: 'scatter',
                mode: 'markers',
                marker: {color: 'yellow', symbol: 'arrow-bar-down', size:11,
                            line: {color: 'black', width:1}
                        },
                name: 'event losses'
            }
            traces.push(trace_event_losses)

            const trace_event_nonlosses = {
                x: dataEventNonLosses.x,
                y: dataEventNonLosses.y,
                text: dataEventLosses.text,
                type: 'scatter',
                mode: 'markers',
                marker: {color: 'yellow', symbol: 'star', size:11,
                            line: {color: 'black', width:1}
                        },
                name: 'event non losses'
            }
            traces.push(trace_event_nonlosses)

            // const trace_event = {
            //     x: this.props.wellPPPData.EVENT.EVENT_PLOT_SG,
            //     y: this.props.wellPPPData.EVENT.EVENT_PLOT_TVDSS_M,
            //     text: this.props.wellPPPData.EVENT.EVENT_DETAIL,
            //     type: 'scatter',
            //     mode: 'markers',
            //     marker: {color: 'yellow', symbol: 'star', size:9,
            //                 line: {color: 'black', width:1}
            //             },
            //     name: 'event'
            // }
            // traces.push(trace_event)
            
            // let eventSymbols = []
            // this.props.wellPPPData.EVENT.EVENT_TYPE.forEach(el=>{
            //     if (el==='losses') {
            //         eventSymbols.push('⭍')
            //     } else {
            //         eventSymbols.push('★')
            //     }
            // })

            // const trace_event = {
            //     x: this.props.wellPPPData.EVENT.EVENT_PLOT_SG,
            //     y: this.props.wellPPPData.EVENT.EVENT_PLOT_TVDSS_M,
            //     text: this.props.wellPPPData.EVENT.EVENT_DETAIL,
            //     type: 'scatter',
            //     mode: 'text',
            //     text: eventSymbols,
            //     textfont: {
            //         size: 25,
            //         color: '#F6C82C', line: {color: 'black', width:1}
            //       },
            //     textposition: 'middle',
            //     bordercolor: 'red',
            //     borderwidth: 2,
            //     borderpad: 4,

            //     name: 'event'
            // }
            // traces.push(trace_event)

        }
        return (
          <Plot
            className="cppp-plotly-component"
            data={traces}
            config={{ scrollZoom:true }}
            layout={ layout_template }
            useResizeHandler={true}
            style={{height: '100%', width: '100%'}}
          />
        );
      }
}

class CorrelationPPPlotDesc extends React.Component {
    constructor(props) {
        super(props)
    }

    // async downloadPPP(wellName) {
    //     try {
    //         const dataParam = {wellName: wellName}
    //         const resp = await axios({
    //             method: 'POST',
    //             url: 'http://localhost:5000/downloadppppost',
    //             data: dataParam,
    //             responseType: 'blob'
    //         });
    //         FileSaver.saveAs(resp.data, resp.headers['x-filename']);
    
    //     } catch (err) {
    //         console.error(err);
    //     } 
    // }

    render() {
        let cell_well_name = "-";
        let cell_sonic_status = "-";
        let cell_td_marker = "-";
        let cell_td_mw = "-";
        let cell_marker_mw = "-";

        if (!isEmpty(this.props.summRecord)) {
            cell_well_name = this.props.summRecord.SHORT_NAME;
            cell_sonic_status = this.props.summRecord.SONIC_FLAG === 'Y' ? "sonic":"no sonic";
            cell_td_marker = "TD " + this.props.summRecord.TD_TVDSS_M + " at " + this.props.summRecord.TD_MARKER;
            cell_td_mw = "MW at TD " + this.props.summRecord.TD_MW_SG;
            cell_marker_mw = "MW at " + this.props.summRecord.PS_TD_MARKER + " " + this.props.summRecord.PS_TD_MW_SG;
        }

        return(
            <table className="cppp-desc-table-table">
                <tbody>
                    <tr className="cppp-desc-table-tr">
                        <td className="cppp-desc-table-td">{cell_well_name}</td>
                    </tr>
                    <tr className="cppp-desc-table-tr">
                        <td className="cppp-desc-table-td">{cell_sonic_status}</td>
                    </tr>
                    <tr className="cppp-desc-table-tr">
                        <td className="cppp-desc-table-td">{cell_td_marker}</td>
                    </tr>
                    <tr className="cppp-desc-table-tr">
                        <td className="cppp-desc-table-td">{cell_td_mw}</td>
                    </tr>
                    <tr className="cppp-desc-table-tr">
                        <td className="cppp-desc-table-td">{cell_marker_mw}</td>
                    </tr>
                    {/* <tr className="cppp-desc-table-tr">
                        <td className="cppp-desc-table-td">
                            <button className='cppp-download-btn' onClick={()=>{this.downloadPPP(this.props.summRecord.SHORT_NAME)}}>Download as csv</button>
                        </td>
                    </tr> */}
                </tbody>
            </table>
        );
    }
}


class CorrelationTabContent extends React.Component{

    constructor(props){
        super(props)
    }

    render() {
        if (this.props.selectedWellsPMPPP.length===0) {
            return(
                <></>
            );
        } else {
            return(
                <>
                    { 
                        this.props.selectedWellsPMPPP.map((selectedWellPMPPP, i) => {
    
                            return (
                            
                                <div key={i} className='correlationpp-plot-container'>
                                    <div className='correlationpp-plot-plotly-container'>
                                        <CorrelationPPPlotPlotly
                                            wellPPPData={selectedWellPMPPP}
                                            // summRecord={this.props.summRecords[i]}
                                        />
                                    </div>
                                    <div className='correlationpp-plot-desc-container'>
                                        <CorrelationPPPlotDesc 
                                            summRecord={this.props.selectedSummRecords[i]}
                                        />
                                    </div>
                                </div>
                            );         
                        })
                    }
                </>        
            );
        }
    }
}

export default CorrelationTabContent;