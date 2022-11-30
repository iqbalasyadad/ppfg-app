import React from "react";
import {matchSorter} from 'match-sorter' 
import { useTable, useFilters, useBlockLayout, useRowSelect } from "react-table";
import { useSticky } from "react-table-sticky";
import styled from "styled-components";
import "./SummaryTabContent.css"

function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}

function generateHeaderText(propWell) {
  if (!isEmpty(propWell)) {
    let headerText = propWell.well_name;
    headerText += " TD " + propWell.TD.z + " Top "+ propWell.TD.marker_name;
    headerText += " at " + propWell.TD.marker_depth + " + " + propWell.TD.marker_plus +" mTVDSS";
    return (headerText);
  } else {
    return ("");
  }
}

const SummaryTableStyles = styled.div`
  padding: 1rem;
  max-width: 100%;
  max-height: 100%;

  .table {
    border: 1px solid #ddd;

    .tr {
      :last-child {
        .td {
          border-bottom: 0;
        }
      }
    }

    .th,
    .td {
      padding: 5px;
      border-bottom: 1px solid #ddd;
      border-right: 1px solid #ddd;
      border-left: 1px solid #ddd;

      background-color: #fff;
      overflow: hidden;
      font-size: 9pt;

      :last-child {
        border-right: 0;
      }

      .resizer {
        display: inline-block;
        width: 5px;
        height: 100%;
        position: absolute;
        right: 0;
        top: 0;
        transform: translateX(50%);
        z-index: 1;

        &.isResizing {
          background: black;
        }
      }
    }

    &.sticky {
      overflow: scroll;
      .header,
      .footer {
        position: sticky;
        z-index: 1;
        width: fit-content;
      }

      .header {
        top: 0;
        box-shadow: 0px 3px 3px #ccc;
      }

      .footer {
        bottom: 0;
        box-shadow: 0px -3px 3px #ccc;
      }

      .body {
        position: relative;
        z-index: 0;
      }

      [data-sticky-td] {
        position: sticky;
      }

      [data-sticky-last-left-td] {
        box-shadow: 2px 0px 3px #ccc;
      }

      [data-sticky-first-right-td] {
        box-shadow: -2px 0px 3px #ccc;
      }
    }
  }
`;

// Define a default UI for filtering
function DefaultColumnFilter({
  column: { filterValue, preFilteredRows, setFilter },
}) {
  const count = preFilteredRows.length

  return (
    <input style={{ border:'1px solid gray'}}
      value={filterValue || ''}
      onChange={e => {
        setFilter(e.target.value || undefined) // Set undefined to remove the filter entirely
      }}
      placeholder={`search`} size='5'
    />
  )
}

const IndeterminateCheckbox = React.forwardRef(
    ({ indeterminate, ...rest }, ref) => {
      const defaultRef = React.useRef();
      const resolvedRef = ref || defaultRef;
  
      React.useEffect(() => {
        resolvedRef.current.indeterminate = indeterminate;
      }, [resolvedRef, indeterminate]);
  
      return (
        <>
          <input type="checkbox" ref={resolvedRef} {...rest} />
        </>
      );
    }
);

function fuzzyTextFilterFn(rows, id, filterValue) {
  return matchSorter(rows, filterValue, { keys: [row => row.values[id]] })
}

// Let the table remove the filter if the string is empty
fuzzyTextFilterFn.autoRemove = val => !val

function SummaryTable({ columns, data, onRowSelectStateChange }) {

  const filterTypes = React.useMemo(
    () => ({
      // Add a new fuzzyTextFilterFn filter type.
      fuzzyText: fuzzyTextFilterFn,
      // Or, override the default text filter to use
      // "startWith"
      text: (rows, id, filterValue) => {
        return rows.filter(row => {
          const rowValue = row.values[id]
          return rowValue !== undefined
            ? String(rowValue)
                .toLowerCase()
                .startsWith(String(filterValue).toLowerCase())
            : true
        })
      },
    }),
    []
  );

  const defaultColumn = React.useMemo(
      () => ({
        minWidth: 0,
        width: 30,
        maxWidth: 1000,
        Filter: DefaultColumnFilter,
      }),
      []
  );

  // Use the state and functions returned from useTable to build your UI
  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    // selectedFlatRows,
    state: { selectedRowIds },
  } = useTable(
    {
      columns,
      data,
      defaultColumn,
      filterTypes
    },
    useBlockLayout,
    useSticky,
    useFilters,
    useRowSelect,
  );

  // Row-select state change
  React.useEffect(() => onRowSelectStateChange?.(selectedRowIds), [
      onRowSelectStateChange,
      selectedRowIds
  ]);

  return (
      <div
        {...getTableProps()}
        className="table sticky"
        style={{ height: 700 }}
        >
        <div className="header">
          {headerGroups.map(headerGroup => (
            <div {...headerGroup.getHeaderGroupProps()} className="tr">
              {headerGroup.headers.map(column => (
                <div {...column.getHeaderProps({
                  style: { minWidth: column.minWidth, width: column.width, textAlign: 'center' },
                })} className="th">
                  {column.render("Header")}
                  <div>{column.canFilter ? column.render('Filter') : null}</div>
                </div>
              ))}
            </div>
          ))}
        </div>

        <div {...getTableBodyProps()} className="body">
          {rows.map((row, i) => {
            prepareRow(row);
            return (
              <div {...row.getRowProps()} className="tr">
                {row.cells.map(cell => {
                  return (
                    <div {...cell.getCellProps()} className="td">
                      {cell.render("Cell")}
                    </div>
                  );
                })}
              </div>
            );
          })}
        </div>
      </div>
  );
}

function SummaryTabContent(props) {
    const columns = React.useMemo(
        () => [
            {
                Header: ".",
                width: 30,
                sticky: "left",
                columns: [
                    {
                        id: "selection",
                        Header: ({ getToggleAllRowsSelectedProps }) => (
                        <div>
                            <IndeterminateCheckbox {...getToggleAllRowsSelectedProps()} />
                        </div>
                        ),
                        Cell: ({ row }) => (
                        <div>
                            <IndeterminateCheckbox {...row.getToggleRowSelectedProps()} />
                        </div> )
                    }
                ]
            },
            {
                Header: "..",
                width: 100,
                sticky: "left",
                columns: [
                  {
                    Header: "Well Name",
                    accessor: 'SHORT_NAME',
                    width: 100,
                    filter: 'fuzzyText',
                  },
                ]
            },
            {
            Header: "...",
            width: 130,
            columns: [
                {
                Header: "Section TD (inch)",
                accessor: 'TD_SECTION_INCH',
                width: 130,
                disableFilters:true
                }
            ]
            },
            {
            Header: "Well TD",
            width: 300,
            columns: [
                {
                Header: "Depth (mTVDSS)",
                accessor: "TD_TVDSS_M",
                width: 100,
                disableFilters:true
                },
                {
                Header: "Layer",
                accessor: "TD_MARKER",
                width: 100,
                disableFilters:true
                },
                {
                Header: "MW (sg)",
                accessor: "TD_MW_SG",
                width: 100,
                disableFilters:true
                }
            ]
            },
            {
            Header: "....",
            width: 100,
            columns: [{
                Header: "Distance (km)",
                accessor: 'DIST_KM',
                width: 100,
                disableFilters:true
            }]

            },
            {
            Header: "At Proposed Well TD",
            width: 300,
            columns: [
                {
                Header: "Depth (mTVDSS)",
                accessor: "PS_TD_TVDSS_M",
                width: 100,
                disableFilters:true
                },
                {
                Header: "Layer",
                accessor: "PS_TD_MARKER",
                width: 100,
                disableFilters:true
                },
                {
                Header: "MW (sg)",
                accessor: "PS_TD_MW_SG",
                width: 100,
                disableFilters:true
                }
            ]
            },
            {
            Header: ".....",
            width: 100,
            columns: [{
                Header: "Sonic",
                accessor: 'SONIC_FLAG',
                width: 100,
                disableFilters:true,
                Cell: props => (
                <div style={{
                    backgroundColor: props.value === "Y" ? "green" : "",
                    textAlign: 'center'
                    }}>
                    <span style={{ 
                    color: props.value === "Y" ? "white" : "",
                    textAlign: 'center'
                    }}>
                    {props.value} 
                    </span>
                </div>
                ),
            }]

            },
            {
            Header: "......",
            width: 100,
            columns: [{
                Header: "PP Post Mortem",
                accessor: 'POST_MORTEM_FLAG',
                width: 100,
                disableFilters:true,
                Cell: props => (
                <div style={{
                    backgroundColor: props.value === "Y" ? "green" : "",
                    textAlign: 'center'
                    }}>
                    <span style={{ 
                    color: props.value === "Y" ? "white" : "", 
                    }}>
                    {props.value} 
                    </span>
                </div>
                ),
            }]

            },
            {
            Header: ".......",
            width: 100,
            columns: [{
                Header: "SPUD Date",
                accessor: 'SPUD_DATE',
                width: 100,
                disableFilters:true,
            }]
            },
            {
            Header: "........",
            width: 100,
            columns: [{
                Header: "Event",
                accessor: 'EVENT_FLAG',
                enableRowSpan: true,
                width: 100,
                disableFilters:true,
                Cell: props => (
                <div style={{
                    backgroundColor: props.value === "Y" ? "red" : "",
                    textAlign: 'center'
                    }}>
                    <span style={{ 
                    color: props.value === "Y" ? "white" : "", 
                    }}>
                    {props.value} 
                    </span>
                </div>
                ),
            }]

            },
            // {
            //   Header: "LCT",
            //   accessor: 'LCT'
            // }, 
            {
            Header: ".........",
            width: 500,
            columns: [
                {
                Header: "Event Remark",
                accessor: 'EVENT_SHORT_DESC',
                width: 500,
                disableFilters:true
                },
            ]
            },
        ],
      []
    );


    const data = React.useMemo(() => props.summRecords, [props.summRecords] )
  
    const [selectedRowIds, setSelectedRowIds] = React.useState({});
    const [unorderedSelectedRowIds, setUnorderedSelectedRowIds] = React.useState([]);

    const [lastSelectedRowKeysId, setLastSelectedRowKeysId] = React.useState([]);


    const selectedRowKeysId = Object.keys(selectedRowIds).map(key => parseInt(key));

    if (!(lastSelectedRowKeysId.length === selectedRowKeysId.length && lastSelectedRowKeysId.every((value, index) => value === selectedRowKeysId[index]))) {
      if (selectedRowKeysId.length === props.summRecords.length) {
        setUnorderedSelectedRowIds(selectedRowKeysId)
      }
      setLastSelectedRowKeysId(selectedRowKeysId)
    }
    else {
      selectedRowKeysId.forEach(el=>{
        if (!unorderedSelectedRowIds.includes(el)){
          setUnorderedSelectedRowIds([...unorderedSelectedRowIds, el])
        }
      })
    }

    // selectedRowKeysId.forEach(el=>{
    //   if (!unorderedSelectedRowIds.includes(el)){
    //     setUnorderedSelectedRowIds([...unorderedSelectedRowIds, el])
    //   }
    // })

    if (selectedRowKeysId.length < unorderedSelectedRowIds.length) {
      let selectedFinals = []
      unorderedSelectedRowIds.forEach(el=>{
        if (selectedRowKeysId.includes(el)){
          selectedFinals.push(el)
        }
      })
      setUnorderedSelectedRowIds(selectedFinals)
    }

    const unOrderedWellNames = unorderedSelectedRowIds.map( keyId => {
      return (props.surrWells[keyId])
    })
    
    if (props.summRecords.length===0) {
      return(
        <></>
      );
    } else {
      return (
        <div className="summary-content-item-child" >
          <div className='summary-header-container'>
            <div id='sh-p-wname'> <span>{generateHeaderText(props.propWell)}</span> </div>      
          </div>
          <div className='summary-content-item-table'>
            <SummaryTableStyles>
              <SummaryTable
                columns={columns}
                data={data}
                onRowSelectStateChange={setSelectedRowIds}
              />
            </SummaryTableStyles>
          </div>
          <div>
              <button className="summary-select-wells-apply-btn" disabled={props.summBtnDisabled}
                onClick={()=>{props.onSubmitWells(unOrderedWellNames)}}>Correlate and Combine Post Mortem</button>
          </div>
        </div>
  
      );
    }
}

export default SummaryTabContent;