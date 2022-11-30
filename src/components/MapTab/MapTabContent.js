import React from "react";
import './MapTabContent.css'

import axios from 'axios'

import MapPlot from './MapPlot'
import MapSettings from "./MapSettings"; 

function isEmpty(obj) {
    return Object.keys(obj).length === 0;
}

class MapTabContent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            wellsPos: {},
            wellsTrajectory: [],
            hideMapWSettings: true,
            fieldName: '',
            mapMarker: 'MF2',
            mapSettingsData: {},
            sWellRecords: {},
            markerOptions: [],
            wellOptions: []
        }
        this.onChangeMapField = this.onChangeMapField.bind(this);
        this.onChangeMapMarker = this.onChangeMapMarker.bind(this);
        this.handleMapSettingsSubmit = this.handleMapSettingsSubmit.bind(this);
        this.handleMapResetSubmit = this.handleMapResetSubmit.bind(this);

    }
    
    async getWellsPos(fieldName, mapMarker) {
        try {
            const data = {
                map_marker: mapMarker,
                map_field: fieldName
            }
            const resp = await axios.post('http://localhost:5000//getwellmarkerpos', data);
            this.setState({wellsPos: resp.data})
        } catch (err) {
            console.error(err);
        }
    }
    async getWellsTrajectory(fieldName) {
        try {
            const resp = await axios.post('http://localhost:5000//gettrajectory', {map_field: fieldName});
            this.setState({wellsTrajectory: resp.data})
        } catch (err) {
            console.error(err);
        }
    }

    async getMarkerSelectOptions(fieldName){
        const res = await axios.post('http://localhost:5000/getfieldmarkername', {map_field: fieldName})
        const data = res.data

        const options = data.map(d => ({
            "value" : d.MARKER_NAME,
            "label" : d.MARKER_NAME
        }))
        this.setState({markerOptions: options})
    }
    async getWellSelectOptions(fieldName){
        const res = await axios.post('http://localhost:5000/getfieldwellname', {map_field: fieldName})
        const data = res.data

        const options = data.map(d => ({
            "value" : d.SHORT_NAME,
            "label" : d.SHORT_NAME
        }))
        this.setState({wellOptions: options})
    }

    onChangeMapField(childValue) {
        this.setState({ fieldName: childValue,  wellsPos: {}})
        this.getWellsTrajectory(childValue)
        this.getMarkerSelectOptions(childValue)
        this.getWellSelectOptions(childValue)
    }

    onChangeMapMarker(mapMarker) {
        this.setState({ mapMarker: mapMarker })
        this.getWellsPos(this.state.fieldName, mapMarker)
    }

    handleMapSettingsSubmit(childValue) {
        childValue.fieldName = this.state.fieldName;
        childValue.mapMarker = this.state.mapMarker;
        this.props.onMapSettingsSubmit(childValue)
    }
    handleMapResetSubmit(childValue) {
        this.props.onMapResetSubmit(childValue)
    }

    // componentDidMount() {
    //     this.getWellsTrajectory()
    // }

    render() {
        return (
            <div style={{height:'100%', width:'100%'}}>
                <MapSettings
                    fieldName={this.state.fieldName}
                    markerOptions={this.state.markerOptions}
                    wellOptions={this.state.wellOptions}
                    onChangeMapField={this.onChangeMapField}
                    onChangeMapMarker={this.onChangeMapMarker}
                    onMapSettingsSubmit={this.handleMapSettingsSubmit}
                    onMapResetSubmit={this.handleMapResetSubmit}

                />
                <MapPlot 
                    well_trajectory={this.state.wellsTrajectory}
                    well_pos={this.state.wellsPos} 
                    surrSettings={this.props.surrSettings} 
                    summRecords={this.props.summRecords}
                    selectedSummWells={this.props.selectedSummWells}
                />
            </div>
        );
    }
  }
  
  export default MapTabContent;