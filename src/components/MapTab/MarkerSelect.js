import React from "react"
import Select from 'react-select';
import axios from 'axios'

const customStyles = {
    control: (provided, state) => ({
        ...provided,
        background: '#fff',
        borderColor: '#9e9e9e',
        minHeight: '25px',
        height: '25px',
        boxShadow: state.isFocused ? null : null,
    }),

    valueContainer: (provided, state) => ({
        ...provided,
        height: '25px',
        padding: '0px 5px 5px 5px'
    }),

    input: (provided, state) => ({
        ...provided,
        margin: '0px',
    }),
    indicatorSeparator: state => ({
        display: 'none',
    }),
    indicatorsContainer: (provided, state) => ({
        ...provided,
        height: '25px',
    }),
};

class MarkerSelect extends React.Component {
    constructor(props){
        super(props)
        this.state = {
            selectOptions : [],
            id: "",
            name: ''
        }
    }
    async getOptions(fieldName){
        const res = await axios.post('http://localhost:5000/getfieldmarkername', {map_field: fieldName})
        const data = res.data

        const options = data.map(d => ({
            "value" : d.MARKER_NAME,
            "label" : d.MARKER_NAME
        }))
        this.setState({selectOptions: options})
    }
    
    handleChange(e){
        this.setState({id:e.value, name:e.label})
        const newValue = e.value;
        this.props.onChangeMapMarker(newValue );
    }

    // componentDidMount(){
    //     console.log(this.props.fieldName);
    //     this.getOptions(this.props.fieldName);
    // }

    render() {
        return (
          <div style={{width:'100%'}}>
            <Select 
                styles={customStyles}
                // options={this.state.selectOptions} 
                options={this.props.markerOptions} 
                onChange={this.handleChange.bind(this)}
            />
          </div>
        )
    }
}

export default MarkerSelect;