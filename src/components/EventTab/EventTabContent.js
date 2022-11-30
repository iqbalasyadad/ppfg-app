import React from 'react'
import {matchSorter} from 'match-sorter' 
import { useTable, useFilters, useBlockLayout } from "react-table";
import { useSticky } from "react-table-sticky";
import styled from "styled-components";
import './EventTabContent.css'

const EventTableStyles = styled.div`
  padding: 1rem;
  max-width: 100%;
  max-height: 100%;
  .table {
    border: 1px solid #ddd;
    background-color: white;
    
    .tr {
      :last-child {
        .td {
          border-bottom: 0;
        }
      }
    }

    .th {
      padding: 5px;
      font-size: 9pt;
      text-align: center;
      border-bottom: 1px solid #ddd;
      border-right: 1px solid #ddd;
      background-color: white;
    },
    .td {
      padding: 5px;
      border-bottom: 1px solid #ddd;
      border-right: 1px solid #ddd;
      background-color: #fff;
      overflow: hidden;
      font-size: 9pt;
      background-color: white;

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
          background: red;
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

function fuzzyTextFilterFn(rows, id, filterValue) {
  return matchSorter(rows, filterValue, { keys: [row => row.values[id]] })
}

// Let the table remove the filter if the string is empty
fuzzyTextFilterFn.autoRemove = val => !val

function EventTable({ columns, data }) {

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
      minWidth: 150,
      width: 150,
      maxWidth: 800,
      Filter: DefaultColumnFilter,
    }),
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow
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
  );
  
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
                <div {...column.getHeaderProps()} className="th">
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

function EventTabContent(props) {
    const columns = React.useMemo(
        () => [
        {
          Header: "Well Name",
          accessor: "SHORT_NAME",
          sticky: "left",
          width: 80,
          filter: 'fuzzyText',
        },
        {
          Header: 'PLOT SG',
          accessor: 'EVENT_PLOT_SG',
          width: 80,
          disableFilters:true,
        },
        {
          Header: 'PLOT TVDSS',
          accessor: 'EVENT_PLOT_TVDSS_M',
          width: 80,
          disableFilters:true,
        },
        {
          Header: 'TVDSS',
          accessor: 'EVENT_TVDSS_M',
          width: 80,
          disableFilters:true,
        },
        {
          Header: 'REMARK',
          accessor: 'EVENT_DETAIL',
          width: 100,
          disableFilters:true,
        },
        {
          Header: 'DESCRIPTION',
          accessor: 'EVENT_DESCRIPTION',
          width: 700,
          disableFilters:true,
        },
        ],
        []
    )
    const data = React.useMemo(() => props.eventRecords)

    if (props.surrWells.length===0) {
      return(
        <></>
      );    
    } else {
      return (
        <div className='event-content-item-table' >
            <EventTableStyles>
                <EventTable 
                    columns={columns}
                    data={data}
                />
            </EventTableStyles>
        </div>
      )
    }

}


export default EventTabContent;