import React from "react";
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';


import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faGear } from '@fortawesome/free-solid-svg-icons'

import FieldSelect from './FieldSelect'
import MarkerSelect from './MarkerSelect'
import WellSelect from './WellSelect'


class MapSettings extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hideMapWSettings: false,
            pTDX: '',
            pTDY: '',
            pWell: '',
            sRadius: 2000,
            mode: ''
        }
        this.setHideMapWSettings = this.setHideMapWSettings.bind(this);
        this.onChangeMapField = this.onChangeMapField.bind(this);
        this.onChangeMapMarker = this.onChangeMapMarker.bind(this);
        this.handleChangePWell = this.handleChangePWell.bind(this);
        this.handleChangePTDX = this.handleChangePTDX.bind(this);
        this.handleChangePTDY = this.handleChangePTDY.bind(this);
        this.handleChangeSRadius = this.handleChangeSRadius.bind(this);
        this.handlePointSubmit = this.handlePointSubmit.bind(this);
        this.handleWellSubmit = this.handleWellSubmit.bind(this);
        this.handleWellReset = this.handleWellReset.bind(this);

    }
    
    setHideMapWSettings(hidestate) {
        this.setState({ hideMapWSettings: hidestate })
    }

    onChangeMapField(childValue) {
        this.props.onChangeMapField(childValue);
    }
    onChangeMapMarker(childValue) {
        this.props.onChangeMapMarker(childValue);
    }
    handleChangePWell(childValue) {
        this.setState({pWell:childValue});
    }
    handleChangePTDX(event) {
        this.setState({pTDX: parseInt(event.target.value)});
    }
    handleChangePTDY(event) {
        this.setState({pTDY: parseInt(event.target.value)});
    }
    handleChangeSRadius(event) {
        this.setState({sRadius: parseInt(event.target.value)});
    }
    handlePointSubmit(event) {
        const formData = {
            mode: 'point',
            pTDX: this.state.pTDX,
            pTDY: this.state.pTDY,
            sRadius: this.state.sRadius,
        }
        this.props.onMapSettingsSubmit(formData);

        event.preventDefault();
    }
    handleWellSubmit(event) {
        const formData = {
            mode: 'well',
            pWell: this.state.pWell,
            sRadius: this.state.sRadius,
        }
        this.props.onMapSettingsSubmit(formData);
        event.preventDefault();
    }
    handleWellReset(event) {
        this.props.onMapResetSubmit('');
        event.preventDefault();

    }
    render() {
        return(
            <div className="map-well-settings-container-parent">
                <button className="map-w-setting-collapse-btn" 
                    onClick={()=>this.setHideMapWSettings(!this.state.hideMapWSettings)}>
                        <FontAwesomeIcon icon={faGear} className='map-settings-collapse-icon'/>
                </button>
                <div className={`map-well-settings-container ${this.state.hideMapWSettings?"hide-map-well-settings-container": ""}`}>
                    <div className="map-well-settings-header">
                        <span>Settings</span>
                    </div>
                    <div className="map-well-settings-content">
                        <div className="msb-form-container">

                            <div className='sinput-form-group-container'>
                                <div className='sinput-form-group-label'>
                                    <label htmlFor="i-fg-label">Field Name</label>
                                </div>
                                <div className='sinput-form-group-input'>
                                    <FieldSelect onChangeMapField={this.onChangeMapField}/>
                                </div>
                            </div>

                            <div className='sinput-form-group-container'>
                                <div className='sinput-form-group-label'>
                                    <label htmlFor="i-fg-label">Map Marker</label>
                                </div>
                                <div className='sinput-form-group-input'>
                                    <MarkerSelect 
                                        // fieldName={this.props.fieldName} 
                                        markerOptions={this.props.markerOptions}
                                        onChangeMapMarker={this.onChangeMapMarker}
                                    />
                                </div>
                            </div>

                            <Tabs
                                style={{fontSize: '10pt', color: 'black'}}
                                id="controlled-tab-example"
                                defaultActiveKey="point"
                                className="mb-3"
                                fill
                                >
                                <Tab eventKey="point" title="Point" >

                                    <form onSubmit={this.handlePointSubmit}>

                                        <div className='sinput-form-group-container'>
                                            <div className='sinput-form-group-label'>
                                                <label htmlFor="i-fg-label">X</label>
                                            </div>
                                            <div className='sinput-form-group-input'>
                                                <input className='sinput-form-group-input-text' type="number" value={this.state.pTDX} onChange={this.handleChangePTDX} required="required"/>
                                            </div>
                                        </div>

                                        <div className='sinput-form-group-container'>
                                            <div className='sinput-form-group-label'>
                                                <label htmlFor="i-fg-label">Y</label>
                                            </div>
                                            <div className='sinput-form-group-input'>
                                                <input className='sinput-form-group-input-text' type="number" value={this.state.pTDY} onChange={this.handleChangePTDY} required="required"/>
                                            </div>
                                        </div>

                                        <div className='sinput-form-group-container'>
                                            <div className='sinput-form-group-label'>
                                                <label htmlFor="i-fg-label">Radius</label>
                                            </div>
                                            <div className='sinput-form-group-input'>
                                                <input className='sinput-form-group-input-text' type="number" value={this.state.sRadius} onChange={this.handleChangeSRadius} required="required"/>
                                            </div>
                                        </div>

                                        <div className='sinput-form-group-container'>
                                            <div className='sinput-form-group-label'>
                                                <label htmlFor="i-fg-label"></label>
                                            </div>
                                            <div className='sinput-form-group-input'>
                                                <input className='map-settings-reset-btn' type="button" value="Reset" onClick={this.handleWellReset} />
                                            </div>
                                            <div className='sinput-form-group-input'>
                                                <input className='map-settings-submit-btn' type="submit" value="Apply" />
                                            </div>
                                        </div>
                                        
                                    </form>
                                </Tab>
                                <Tab eventKey="well" title="Well">

                                    <form onSubmit={this.handleWellSubmit}>
                                        <div className='sinput-form-group-container'>
                                            <div className='sinput-form-group-label'>
                                                <label htmlFor="i-fg-label">Well</label>
                                            </div>
                                            <div className='sinput-form-group-input'>
                                                <WellSelect
                                                    wellOptions={this.props.wellOptions} 
                                                    onChangePWell={this.handleChangePWell}
                                                />
                                            </div>
                                        </div>

                                        <div className='sinput-form-group-container'>
                                            <div className='sinput-form-group-label'>
                                                <label htmlFor="i-fg-label">Radius</label>
                                            </div>
                                            <div className='sinput-form-group-input'>
                                                <input className='sinput-form-group-input-text' type="number" value={this.state.sRadius} onChange={this.handleChangeSRadius} required="required"/>
                                            </div>
                                        </div>

                                        <div className='sinput-form-group-container'>
                                            <div className='sinput-form-group-label'>
                                                <label htmlFor="i-fg-label"></label>
                                            </div>
                                            <div className='sinput-form-group-input'>
                                                <input className='map-settings-reset-btn' type="button" value="Reset" onClick={this.handleWellReset} />
                                            </div>
                                            <div className='sinput-form-group-input'>
                                                <input className='map-settings-submit-btn' type="submit" value="Apply" />
                                            </div>

                                        </div>
                                    </form>

                                </Tab>
                            </Tabs>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

export default MapSettings;