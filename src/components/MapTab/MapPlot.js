import React from "react";
import Plot from 'react-plotly.js';

function get2PointCircle(center_x, center_y, radius) {
    const point_1_x = center_x - radius;
    const point_1_y = center_y - radius;

    const point_2_x = center_x + radius;
    const point_2_y = center_y + radius;

    const points = {
        x: [point_1_x, point_2_x],
        y: [point_1_y, point_2_y]
    }
    return points;
}

function isEmpty(obj) {
  try {
      let objtest = Object.keys(obj).length === 0;
  } catch(error) {
      return true;
  }
  return Object.keys(obj).length === 0;
}

class MapPlot extends React.Component {
  constructor(props) {
    super(props)
  }


  render() {

    let traces = []

    const layout_template = { dragmode: 'pan', autosize: true, title: false, margin:{l:20, r:10, b:20, t:10},
      legend:{ x: 1, xanchor: 'right', y: 0, borderwidth:1},
      font: { size: 8 },
      xaxis:{autorange: true, range: [], title:false, showgrid:false, showline:true, dtick:1000, mirror:'ticks', ticks:'outside', tickcolor:'black',
          minor:{dtick:100, tickcolor:'black', tickwidth:1, showgrid:false}
      },
      yaxis:{autorange: true, range: [], title:false, scaleanchor:'x', showgrid:false, showline:true, dtick:1000, mirror:'ticks', ticks:'outside', tickcolor:'black', tickangle:-90,
          minor:{dtick:100, tickcolor:'black', tickwidth:1, showgrid:false}
      },
      shapes: []
    }

    // add wells trajectory
    if(this.props.well_trajectory.length>0){
      for (var key in this.props.well_trajectory) {
        if (this.props.well_trajectory.hasOwnProperty(key)) {

          // add selected trajectory well line
          const wellTrajectoryPos = { 
            xs:this.props.well_trajectory[key].X, 
            ys:this.props.well_trajectory[key].Y
          };
          // selected wells trace
          const trace_well_trajectory = {
            x: wellTrajectoryPos.xs,
            y: wellTrajectoryPos.ys,
            type: 'scatter',
            mode: 'lines',
            line: { dash: 'dash', color: '#B7B7B7', width: 1,
            },
            showlegend: false,
            hoverinfo: 'skip'
          }
          traces.push(trace_well_trajectory)
        }
      }
    }

    if (!isEmpty(this.props.summRecords)) {
      let event_pos = { xs: [], ys:[], text:[] }
      let dt_pos = { xs: [], ys:[] }
      let shallower_pos = { xs: [], ys:[] }
      let post_mortem_pos = { xs: [], ys:[] }

      for (var key in this.props.summRecords) {
        if (this.props.summRecords.hasOwnProperty(key)) {
          const event_status = this.props.summRecords[key].EVENT_FLAG;
          if (event_status==='Y'){
            event_pos.xs.push(this.props.summRecords[key].WELL_X_M);
            event_pos.ys.push(this.props.summRecords[key].WELL_Y_M);
          }
          const dt_status = this.props.summRecords[key].SONIC_FLAG;
          if (dt_status==='Y'){
            dt_pos.xs.push(this.props.summRecords[key].WELL_X_M);
            dt_pos.ys.push(this.props.summRecords[key].WELL_Y_M);
          }
          const shallower_status = this.props.summRecords[key].PS_SHALLOWER_FLAG;
          if (shallower_status==='Y'){
            shallower_pos.xs.push(this.props.summRecords[key].WELL_X_M);
            shallower_pos.ys.push(this.props.summRecords[key].WELL_Y_M);
          }
          const post_mortem_status = this.props.summRecords[key].POST_MORTEM_FLAG;
          if (post_mortem_status==='Y'){
            post_mortem_pos.xs.push(this.props.summRecords[key].WELL_X_M);
            post_mortem_pos.ys.push(this.props.summRecords[key].WELL_Y_M);
          }
        }
      }
      
      // event trace
      const trace_event = {
        x: event_pos.xs,
        y: event_pos.ys,
        type: 'scatter',
        mode: 'markers',
        marker: {color: 'red', size:15, opacity:0.7},
        name: 'event',
        hoverinfo: 'skip'
      }
      traces.push(trace_event)

      // shallower trace
      const trace_shallower = {
        x: shallower_pos.xs,
        y: shallower_pos.ys,
        type: 'scatter',
        mode: 'markers',
        marker: {color: 'black', symbol: 'x-thin', size:10, line:{width:1, color:'black'}},
        name: 'shallower',
        hoverinfo: 'skip',
        visible: 'legendonly'
      }
      traces.push(trace_shallower)

      // dt trace
      const trace_dt = {
        x: dt_pos.xs,
        y: dt_pos.ys,
        type: 'scatter',
        mode: 'markers',
        marker: {color: 'rgba(17, 157, 255, 0)', size:17, line:{color:'rgb(102, 204, 0, 0.7)', width: 2}},
        name: 'sonic',
        hoverinfo: 'skip'
      }
      traces.push(trace_dt)

      // post mortem trace
      const trace_post_mortem = {
        x: post_mortem_pos.xs,
        y: post_mortem_pos.ys,
        type: 'scatter',
        mode: 'markers',
        marker: {color: 'rgba(17, 157, 255, 0)', size:23, line:{color:'rgb(224, 56, 241, 0.7)', width: 2}},
        name: 'post mortem',
        hoverinfo: 'skip',
        visible: 'legendonly'
      }
      traces.push(trace_post_mortem)

      // add selected summ well line
      let selectedSummWellsPos = { xs:[], ys:[] };
      this.props.selectedSummWells.forEach(selectedSummWell => {
        for (var key in this.props.summRecords) {
          if (this.props.summRecords[key].SHORT_NAME===selectedSummWell) {
            selectedSummWellsPos.xs.push(this.props.summRecords[key].WELL_X_M)
            selectedSummWellsPos.ys.push(this.props.summRecords[key].WELL_Y_M)
          }
        }
      });

      // selected wells trace
      const trace_selected_well = {
        x: selectedSummWellsPos.xs,
        y: selectedSummWellsPos.ys,
        type: 'scatter',
        mode: 'lines',
        line: {
          color: 'red',
          width: 3
        }
      }
      traces.push(trace_selected_well)

    }

    if (!isEmpty(this.props.well_pos)){
      const trace_marker = {
        x: this.props.well_pos.X,
        y: this.props.well_pos.Y,
        type: 'scatter',
        mode: 'markers+text',
        marker: {color: 'black', size:6},
        text: this.props.well_pos.SHORT_NAME,
        textposition: 'bottom right',
        name: 'well',
      }
      traces.push(trace_marker)
    }

    // add proposed well surrounding circle and point
    if (!isEmpty(this.props.surrSettings)){  
      const circle_center = {x:this.props.surrSettings.pTDX, y:this.props.surrSettings.pTDY}
      const surr_radius = this.props.surrSettings.sRadius
      const circle_points = get2PointCircle(circle_center.x, circle_center.y, surr_radius)

      const trace_circle_point = {
        x: [circle_center.x],
        y: [circle_center.y],
        type: 'scatter',
        mode: 'markers',
        marker: {color: '#0880C4', symbol: 'star', size:8, line:{width:1, color:'black'}},
        name: 'TD Proposed',
      }

      const shape_circle_surr = {
        type: 'circle',
        xref: 'x',
        yref: 'y',
        x0: circle_points.x[0],
        y0: circle_points.y[0],
        x1: circle_points.x[1],
        y1: circle_points.y[1],
        line: { width: 1, color: 'blue' }
      }

      traces.push(trace_circle_point);
      layout_template.shapes.push(shape_circle_surr);
      layout_template.xaxis.autorange = false;
      layout_template.yaxis.autorange = false;
      layout_template.xaxis.range = [circle_points.x[0]-50, circle_points.x[1]+50];
      layout_template.yaxis.range = [circle_points.y[0]-50, circle_points.y[1]+50];

    }

    return (

      <Plot
        data={traces}
        layout={layout_template}
        useResizeHandler={true}
        config={{ scrollZoom:true }}
        style={{height: '100%', width: '100%'}}
      />

    );
  }
}

export default MapPlot;