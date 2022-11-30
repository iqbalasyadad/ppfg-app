import React from "react";
import axios from 'axios'
import {matchSorter} from 'match-sorter' 
import FileSaver from 'file-saver';
import { useTable, useFilters, useBlockLayout, useRowSelect } from "react-table";
import { useSticky } from "react-table-sticky";
import styled from "styled-components";
import "./DataTabContent.css"

const DataTabContentFilterGeneralStyles = styled.div`
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
      placeholder={`search`} size='10'
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


function TableFilter({ columns, data, onRowSelectStateChange }) {

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
  )

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
    state: { selectedRowIds }
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
        style={{ height:300 }}
        >
        <div className="header">
          {headerGroups.map(headerGroup => (
            <div {...headerGroup.getHeaderGroupProps()} className="tr">
              {headerGroup.headers.map(column => (
                <div {...column.getHeaderProps({
                  style: { minWidth: column.minWidth, width: column.width, display:'flex' },
                })} className="th">
                  {column.render("Header")}
                  <div style={{paddingLeft: '0.5rem'}}>{column.canFilter ? column.render('Filter') : null}</div>
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

function TableResult({ columns, data, onRowSelectStateChange }) {

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
  )

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
    state: { selectedRowIds }
  } = useTable(
    {
      columns,
      data,
      defaultColumn,
    },
    useBlockLayout,
    useSticky,
    useFilters,
    useRowSelect
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
        style={{ maxHeight:500 }}
        >
        <div className="header">
          {headerGroups.map(headerGroup => (
            <div {...headerGroup.getHeaderGroupProps()} className="tr">
              {headerGroup.headers.map(column => (
                <div {...column.getHeaderProps({
                  style: { minWidth: column.minWidth, width: column.width, display: 'flex'},
                })} className="th">
                  {column.render("Header")}
                  <div style={{paddingLeft: '0.5rem'}}>{column.canFilter ? column.render('Filter') : null}</div>
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

async function getDataList(wellNames, dataTypes) {

    if (wellNames.length===0 || dataTypes.length===0) {
        return ([])
    }

    const param = {
        wellNames: wellNames,
        dataTypes: dataTypes
    }
    try {
        const resp = await axios({
          method: 'POST',
          url: 'http://localhost:5000/getdatalist',
          data: param,
        })
        return resp.data
    } catch (err) {
        console.error(err);
    } 
}

async function downloadResultDataTab(tableResultSelectedRecords) {
  if (tableResultSelectedRecords.length===0) {
      return;
  }
  const param = {
      selectedDatas: tableResultSelectedRecords,
  }
  try {
    const resp = await axios({
      method: 'POST',
      url: 'http://localhost:5000/downloadindatatab',
      data: param,
      responseType: 'blob'
    });
    FileSaver.saveAs(resp.data, resp.headers['x-filename']);
  } catch (err) {
      console.error(err);
  } 
}

function DataTabContent(props) {
   
    const tableWellColumns = React.useMemo(
        () => [
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
                </div>
            )
            },
            {
                Header: "Well Name",
                accessor: "SHORT_NAME",
                maxWidth: 1000,
                minWidth: 200,
                width: 400,
                filter: 'fuzzyText',
            },
      ],
      []
    );

    const tableWellData = React.useMemo(() => props.summRecords, [props.summRecords] )
    const [tableWellSelectedRowIds, setTableWellSelectedRowIds] = React.useState({});

    const tableWellSelectedRowKeysId = Object.keys(tableWellSelectedRowIds).map(key => parseInt(key));
    const tableWellSelectedWellNames = tableWellSelectedRowKeysId.map(el=>props.surrWellNames[el])

    // Filter Data Type
    const tableDataTypeColumns = React.useMemo(
        () => [
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
                </div>
            )
            },
            {
                Header: "Data Type",
                accessor: "DATA_TYPE",
                maxWidth: 1000,
                minWidth: 200,
                width: 400,
                filter: 'fuzzyText',
            },
      ],
      []
    );
    const dataTypesOpt = ['post_mortem_profile_original', 'post_mortem_profile_ascii','log']

    const [tableDataTypeDataTemp, setTableDataTypeDataTemp] = React.useState([
      {
        DATA_TYPE: 'Post Mortem Profile Original',
      },
      {
        DATA_TYPE: 'Post Mortem Profile ASCII',
      },
      {
        DATA_TYPE: 'Log',
      },

    ]);

    const tableDataTypeData = React.useMemo(() => tableDataTypeDataTemp, [tableDataTypeDataTemp] )
    const [tableDataTypeSelectedRowIds, setTableDataTypeSelectedRowIds] = React.useState({});
    const tableDataTypeSelectedRowKeysId = Object.keys(tableDataTypeSelectedRowIds).map(key => parseInt(key));
    const tableDataTypeSelectedTypeNames = tableDataTypeSelectedRowKeysId.map(el=>dataTypesOpt[el])

    // Table result
    const [tableResultRecords, setTableResultRecords] = React.useState([]);

    const tableResultColumns = React.useMemo(
        () => [
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
                </div>
            )
            },
            {
                Header: "File Name",
                accessor: "FILE_NAME",
                maxWidth: 400,
                minWidth: 140,
                width: 400,
                filter: 'fuzzyText',
            },
            {
              Header: "Type",
              accessor: "FILE_TYPE",
              maxWidth: 200,
              minWidth: 50,
              width: 150,
              disableFilters: true,
            },
            {
                Header: "Path",
                accessor: "FOLDER_PATH",
                maxWidth: 1000,
                minWidth: 140,
                width: 1000,
                disableFilters: true,
            },
        ],
        []
    );

    const tableResultData = React.useMemo(() => tableResultRecords, [tableResultRecords] )
    const [tableResultSelectedRowIds, setTableResultSelectedRowIds] = React.useState({});
    const tableResultSelectedRowKeysId = Object.keys(tableResultSelectedRowIds).map(key => parseInt(key));

    const tableResultSelectedRecords = tableResultSelectedRowKeysId.map(el => tableResultRecords[el])

    if (props.surrWellNames.length===0) {
      return(
        <></>
      );
    } else {
      return(
        <>
            <div className="data-content-general-filter-container">
                <div className="data-content-well-filter-container">
                    <DataTabContentFilterGeneralStyles>
                        <TableFilter
                            columns={tableWellColumns}
                            data={tableWellData}
                            onRowSelectStateChange={setTableWellSelectedRowIds}
                        />
                    </DataTabContentFilterGeneralStyles>
                </div>
                <div className="data-content-file-type-filter-container">
                    <DataTabContentFilterGeneralStyles>
                        <TableFilter
                            columns={tableDataTypeColumns}
                            data={tableDataTypeData}
                            onRowSelectStateChange={setTableDataTypeSelectedRowIds}
                        />
                    </DataTabContentFilterGeneralStyles>
                </div>
            </div>
            <div className="data-content-apply-filter-container">
                <button className="data-filter-submit-btn" onClick={()=>{
                    getDataList(tableWellSelectedWellNames, tableDataTypeSelectedTypeNames).then(dataRecords => {
                        setTableResultRecords(dataRecords);                
                    })
            
                    }}>Apply</button>
            </div>

            <br/>

            <div className="data-content-result-file-container">
                <DataTabContentFilterGeneralStyles>
                    <TableResult
                        columns={tableResultColumns}
                        data={tableResultData}
                        onRowSelectStateChange={setTableResultSelectedRowIds}
                    />
                </DataTabContentFilterGeneralStyles>
            </div>
            <div className="data-content-download-result-file-container">
              <button className="data-filter-submit-btn" onClick={()=>{
                downloadResultDataTab(tableResultSelectedRecords) 
              }}>Download</button>
            </div>
        </>
      );
    }
}

export default DataTabContent;
