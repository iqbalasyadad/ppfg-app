import React, { useState, useEffect, useRef  } from "react";

import { useTable, useBlockLayout, useRowSelect } from "react-table";
import { useSticky } from "react-table-sticky";
import styled from "styled-components";

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


function TableFilter({ columns, data, onRowSelectStateChange }) {

    const defaultColumn = React.useMemo(
        () => ({
          minWidth: 0,
          width: 30,
          maxWidth: 1000
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
      selectedFlatRows,
      state: { selectedRowIds }
    } = useTable(
      {
        columns,
        data,
        defaultColumn,
        // autoResetSelectedRows: false,
        // autoResetSelectedCell: false,
        // autoResetSelectedColumn: false,
      },
      useBlockLayout,
      useSticky,
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
          style={{ height:300 }}
          >
          <div className="header">
            {headerGroups.map(headerGroup => (
              <div {...headerGroup.getHeaderGroupProps()} className="tr">
                {headerGroup.headers.map(column => (
                  <div {...column.getHeaderProps({
                    style: { minWidth: column.minWidth, width: column.width },
                  })} className="th">
                    {column.render("Header")}
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

function TableSelectTabContent(props) {
    const columns = React.useMemo(
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
            },
      ],
      []
    );
    // {console.log(props.summRecords)}

    const data = React.useMemo(() => props.summRecords, [props.summRecords] )
  
    /** @type {{[key: number]: boolean}} selectedRowIds */
    const [selectedRowIds, setSelectedRowIds] = React.useState({});
    const [unorderedSelectedRowIds, setUnorderedSelectedRowIds] = React.useState([]);

    const selectedRowKeysId = Object.keys(selectedRowIds).map(key => parseInt(key));
    
    selectedRowKeysId.forEach(el=>{
        if (!unorderedSelectedRowIds.includes(el)){
          setUnorderedSelectedRowIds([...unorderedSelectedRowIds, el])
        }
    })

    if (selectedRowKeysId.length < unorderedSelectedRowIds.length) {
      console.log('smaller')
      let selectedFinals = []
      unorderedSelectedRowIds.forEach(el=>{
        if (selectedRowKeysId.includes(el)){
          selectedFinals.push(el)
        }
      })
      setUnorderedSelectedRowIds(selectedFinals)
    }
  

    const isFirstRender = useRef(true)
    useEffect(() => {
        if (isFirstRender.current) {
        isFirstRender.current = false // toggle flag after first render/mounting
        return;
        }
        // {console.log(selectedRowKeysId)}
        // props.onSelectChange(selectedRowKeysId);
    }, [selectedRowIds])
    
  
    return (
      <>
        <DataTabContentFilterGeneralStyles>
        <TableFilter
          columns={columns}
          data={data}
          onRowSelectStateChange={setSelectedRowIds}
        />
        </DataTabContentFilterGeneralStyles>
        <button onClick={()=>console.log(unorderedSelectedRowIds)}>Apply</button>
      </>

    );
}

export default TableSelectTabContent;