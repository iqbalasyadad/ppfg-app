import React from 'react';
import axios from 'axios'

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faMapLocation, faList, 
          faLinesLeaning, faArrowsToDot,
          faStar, faFileArchive
        } from '@fortawesome/free-solid-svg-icons'

import Nav from 'react-bootstrap/Nav';
import Tab from 'react-bootstrap/Tab';

import TopBar from './components/TopBar/TopBar';
import './App.css';
import MapTabContent from './components/MapTab/MapTabContent';
import SummaryTabContent from './components/SummaryTab/SummaryTabContent';
import CorrelationTabContent from './components/CorrelationTab/CorrelationTabContent';
import CombinedPPPTabContent from './components/CombinedPPPTab/CombinedPPPTabContent';
import EventTabContent from './components/EventTab/EventTabContent';
import DataTabContent from './components/DataTab/DataTabContent';

function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

class App extends React.Component {
  constructor(props){
    super(props)
    this.state = {
      mapSettingsData: {},
      surrSettings: {},
      surrWells: [],
      summRecords: [],
      propWell: {},
      selectedSummWells: [],
      selectedSummRecords: [],
      selectedWellsPMPPP: [],
      combinedMode: "",
      pWell: "",
      pMarker: {},
      combinedPPPAnm: {},
      eventRecords: [],
      summBtnDisabled: false,
    }
    this.handleMapSettingsSubmit = this.handleMapSettingsSubmit.bind(this);
    this.handleMapResetSubmit = this.handleMapResetSubmit.bind(this);

    this.handleSummarySubmitWells = this.handleSummarySubmitWells.bind(this);
  }
  handleMapSettingsSubmit(childValue) {
    this.setState({
      mapSettingsData: childValue,
      combinedMode: childValue.mode
    });
    this.getWellsSummary(childValue);
  }

  handleMapResetSubmit(childValue) {
    this.setState({
      surrSettings: {},
      summRecords: [],
      selectedSummWells: [],
      selectedSummRecords: [],
    });
  }

  filterSummRecords(summRecords, wellNames) {
    let selectedSummRecords = []

    wellNames.forEach(wellName => {
        for (var key in summRecords) {
            var summRecord = summRecords[key];
            if (wellName===summRecord.SHORT_NAME) {
                selectedSummRecords.push(summRecord)
            }
        }      
    });
    return (selectedSummRecords)
  }

  async getWellsSummary(summParam) {
    try {
        const resp = await axios.post('http://localhost:5000/getwellsumm', summParam);
          if (!isEmpty(resp.data)) {
            this.setState({
              surrSettings: resp.data.surrSettings, 
              summRecords: resp.data.summWellRecords,
              surrWells: resp.data.surrWellNames,
              propWell: resp.data.propWell,
            });
            this.getWellsEvent({wellNames: resp.data.surrWellNames});

          } else {
            this.setState({
              surrWells: [],
            });  
          }
    } catch (err) {
        console.error(err);
    } 
  }

  handleSummarySubmitWells(selectedWells) {
    this.setState({selectedSummWells: selectedWells})
    const selectedSummRecords = this.filterSummRecords(this.state.summRecords, selectedWells)
    this.setState({selectedSummRecords: selectedSummRecords})

    this.getWellsPPP({wellNames: selectedWells});

    if (this.state.mapSettingsData.mode==="well") {
      const pWell = this.state.mapSettingsData.pWell;
      this.setState({pWell: pWell})
      this.getWellsCombinedAnm(pWell, selectedWells);
    }

  }

  async getWellsPPP(wellNames) {
    try {
      this.setState({summBtnDisabled: true});
      const resp = await axios.post('http://localhost:5000/getwellppp', wellNames);
        if (!isEmpty(resp.data)) {
          this.setState({
            selectedWellsPMPPP: resp.data.postMortemProfileRecords
          })
          this.setState({summBtnDisabled: false});
          // alert("Success")
        } else {
          this.setState({
            selectedWellsPMPPP: []
          });             
        }
    } catch (err) {
        console.error(err);
    }
  }

  async getWellsCombinedAnm(pWellName, sWellNames) {
    const sendParam = {
      pWellName: pWellName,
      wellNames: sWellNames
    }
    try {
        this.setState({summBtnDisabled: true});
        const resp = await axios.post('http://localhost:5000/getwellcombinedanamorph', sendParam);
        const pMarker = resp.data.pMarker;
        const combinedPPPAnm = resp.data.pppAnm;
        if (!isEmpty(pMarker)) {
          this.setState({
            pMarker: pMarker,
            combinedPPPAnm: combinedPPPAnm
          })
        } else {
          this.setState({
            pMarker: {}
          });             
        }
        this.setState({summBtnDisabled: false});
    } catch (err) {
        console.error(err);
    }
  }

  async getWellsEvent(wellNames) {
    try {
        const resp = await axios.post('http://localhost:5000/geteventsum', wellNames);
          if (!isEmpty(resp.data)) {
            this.setState({
              eventRecords: resp.data
            })
          } else {
            this.setState({
              eventRecords: []
            });             
          }
    } catch (err) {
        console.error(err);
    }
  }
  navClickResize() {
    window.dispatchEvent(new Event('resize'));
  }

  render() {
    return (
      <div className="App">
        <div className="main-container">
          <TopBar />
          <div className="main-area">
            <div className="data-area">
              <Tab.Container id="left-tabs-example" defaultActiveKey="map" transition={false}>
  
                <div style={{display: 'flex', flexDirection:'column', height: '100%', width:'100%'}} >
  
                  <div className='nav-tabs-div'>
                    <Nav variant="tabs" className="justify-content-start" style={{fontSize:'10pt'}}>
                      <Nav.Item >
                        <Nav.Link eventKey="map" onClick={()=> this.navClickResize()}>
                          <FontAwesomeIcon icon={faMapLocation} className='nav-icon'/>Map
                        </Nav.Link>
                      </Nav.Item>

                      <Nav.Item >
                          <Nav.Link eventKey="summary">
                            <FontAwesomeIcon icon={faList} className='nav-icon'/>Summary
                          </Nav.Link>
                      </Nav.Item>

                      <Nav.Item>
                        <Nav.Link eventKey="correlation_pp" onClick={()=> this.navClickResize()}>
                          <FontAwesomeIcon icon={faLinesLeaning} className='nav-icon'/>Correlation Post Mortem
                        </Nav.Link>
                      </Nav.Item>
                      
                      <Nav.Item>
                        <Nav.Link eventKey="combined_pp" onClick={()=> this.navClickResize()}>
                          <FontAwesomeIcon icon={faArrowsToDot} className='nav-icon'/>Combination Post Mortem
                        </Nav.Link>
                      </Nav.Item>

                      <Nav.Item >
                          <Nav.Link eventKey="event">
                            <FontAwesomeIcon icon={faStar} className='nav-icon'/>Event
                          </Nav.Link>
                      </Nav.Item>

                      <Nav.Item>
                        <Nav.Link eventKey="data">
                          <FontAwesomeIcon icon={faFileArchive} className='nav-icon'/>Data
                        </Nav.Link>
                      </Nav.Item>


                    </Nav>
                  </div>
  
                  <div style={{ height: 'calc(100% - 45px)', width:'100%'}}>
                    <Tab.Content style={{height:'100%', width:'100%'}}>
  
                      <Tab.Pane eventKey="map" style={{height:'100%'}}>
                        <div className='map-content-container-parent'>
                          <div className='map-content-container-scroll'>
                            <div className='map-content-item'>
                              <MapTabContent 
                                onMapSettingsSubmit={this.handleMapSettingsSubmit} 
                                onMapResetSubmit={this.handleMapResetSubmit} 
                                surrSettings={this.state.surrSettings}
                                summRecords={this.state.summRecords}
                                selectedSummWells = {this.state.selectedSummWells}
                              />
                            </div>
                          </div>
                        </div>
                      </Tab.Pane>

                      <Tab.Pane eventKey="summary" style={{height:'100%'}}>
                        <div className='summary-content-container-parent'>
                          <div className='summary-content-container-scroll'>
                            <div className='summary-content-item'>
                              <SummaryTabContent
                                surrWells={this.state.surrWells}
                                propWell={this.state.propWell} 
                                summRecords={this.state.summRecords}
                                onSubmitWells={this.handleSummarySubmitWells}
                                summBtnDisabled={this.state.summBtnDisabled}
                              />
                            </div>
                          </div>
                        </div>
                      </Tab.Pane>

                      <Tab.Pane eventKey="event" style={{height:'100%'}}>
                        <div className='event-content-container-parent'>
                          <div className='event-content-container-scroll'>
                            <div className='event-content-item'>
                              <EventTabContent 
                                surrWells={this.state.surrWells}
                                eventRecords={this.state.eventRecords}
                              />
                            </div>
                          </div>
                        </div>
                      </Tab.Pane>
  
                      <Tab.Pane eventKey="correlation_pp" style={{height:'100%', width:'100%'}}>
                      <div className='correlation_pp-content-container-parent'>
                          <div className='correlation_pp-content-container-scroll'>
                            <div className='correlation_pp-content-item'>
                              <CorrelationTabContent
                                selectedWellsPMPPP={this.state.selectedWellsPMPPP}
                                selectedSummRecords={this.state.selectedSummRecords}
                              />                     
                            </div>
                          </div>
                      </div>
                      </Tab.Pane>
                      
                      <Tab.Pane eventKey="combined_pp" style={{height:'100%', width:'100%'}}>
                      <div className='combined_pp-content-container-parent'>
                          <div className='combined_pp-content-container-scroll'>
                            <div className='combined_pp-content-item'>
                              <CombinedPPPTabContent
                                selectedSummWells = {this.state.selectedSummWells}
                                combinedMode={this.state.combinedMode} 
                                pWell={this.state.pWell} 
                                pMarker={this.state.pMarker}
                                selectedWellsPMPPP={this.state.selectedWellsPMPPP}
                                combinedPPPAnm={this.state.combinedPPPAnm} 
                              />
  
                            </div>
                          </div>
                      </div>
                      </Tab.Pane>

                      <Tab.Pane eventKey="data" style={{height:'100%'}}>
                        <div className='data-content-container-parent'>
                          <div className='data-content-container-scroll'>
                            <div className='data-content-item'>
                              <DataTabContent 
                                surrWellNames = {this.state.surrWells}
                                summRecords={this.state.summRecords}
                              />
                            </div>
                          </div>
                        </div>
                      </Tab.Pane>

                    </Tab.Content>

                  </div>
  
                </div>
  
              </Tab.Container>
            </div>
  
          </div>
        </div>
      </div>
    );
  }

}

export default App;
