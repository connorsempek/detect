
def make_spec(df, lower, upper, between, look_back, time_col, measure_col,
              data_fp='data.json'):
  '''
  '''

  spec = {
    "$schema": "https://vega.github.io/schema/vega/v3.0.json",
    "height": 400,
    "padding": 20,
    "width": 700,
    "title": {"text": "Thresholds"},
    
    "signals": [
      {"name": "x", "value": 0},
      {"name": "x2", "value": 700},
      {"name": "y", "value": 1},
      {"name": "lower_signal", "value": lower},
      {"name": "upper_signal", "value": upper},
      {"name": "lower_annot", "value": -0.75},
      {"name": "upper_annot", "value": 0.65}
    ],

    "data": [
      {
        "name": "table",
        "url": data_fp,
        "format":{
          "parse": {measure_col: "number", time_col: "date:'%Y-%m-%d %H:%M:%S'"}
        },
        "transform": [
          {"type": "extent", "field": time_col, "signal": "dates"}
        ]
      },
      {
        "name": "lower",
        "source": "table",
        "transform": [
          {"type": "filter", "expr": "datum.{} < lower_signal".format(measure_col)}
        ]
      },
      {
        "name": "upper",
        "source": "table",
        "transform": [
          {"type": "filter", "expr": "datum.{} > upper_signal".format(measure_col)}
        ]
      }
    ],
   
    "scales": [
      {
        "range": "width",
        "type": "time",
        "name": "x",
        "domain": {
          "field": time_col,
          "data": "table"
        },
        "nice":"hour"
      },
      {
        "domain": {
          "field": measure_col,
          "data": "table"
        },
        "name": "y",
        "zero": True,
        "range": "height",
        "type": "linear",
        "nice": True
      }
    ],
    
    "axes": [
      {
        "scale": "x",
        "orient": "bottom"
      },
      {
        "scale": "y",
        "orient": "left"
      }
    ],

    "marks": [
      {
        "encode": {
          "enter": {
            "y": {
              "field": measure_col,
              "scale": "y"
            },
            "x": {
              "field": time_col,
              "scale": "x"
            },
            "interpolate": {
              "value": "monotone"
            },
            "stroke":{"value":"#74b9ff"}
          }
        },
        "from": {
          "data": "table"
        },
        "type": "line"
      },
      {
        "encode": {
          "enter": {
            "y": {
              "field": measure_col,
              "scale": "y"
            },
            "x": {
              "field": time_col,
              "scale": "x"
            },
            "fill": {"value": "#e74c3c"},
            "opacity": {"value":0.7}
          }
        },
        "from": {
          "data": "lower"
        },
        "type": "symbol"
      },
      {
        "encode": {
          "enter": {
            "y": {
              "field": measure_col,
              "scale": "y"
            },
            "x": {
              "field": time_col,
              "scale": "x"
            },
            "fill": {"value": "#e74c3c"},
            "opacity": {"value":0.7}
          }
        },
        "from": {
          "data": "upper"
        },
        "type": "symbol"
      },
      {
        "type": "text",
        "encode":{
          "update": {
            "text": {"signal": "format(upper_signal, ',.2f')"},
            "baseline": {"value": "middle"},
            "x":{"signal": "x2 + 20"},
            "y": {"scale": "y", "signal": "upper_signal"},
            "fontSize": {"value": 14}
          }
        }
      },
      {
        "type": "text",
        "encode":{
          "update": {
            "text": {"signal": "format(lower_signal, ',.2f')"},
            "baseline": {"value": "middle"},
            "x":{"signal": "x2 + 20"},
            "y": {"scale": "y", "signal": "lower_signal"},
            "fontSize": {"value": 14}
          }
        }
      },
      {
        "type": "rule",
        "encode": {
          "enter": {
            "x": {"value": 0},
            "x2": {"signal": "x2 + 10"},
            "stroke": {"value": "#000"},
            "strokeWidth": {"value": 1.5},
            "strokeDash": {"value": [8,8]}
          },
          "update": {
            "y": {"scale": "y", "signal": "lower_signal"}
          }
        }
      },
      {
        "type": "rule",
        "encode": {
          "enter": {
            "x": {"value": 0},
            "x2": {"signal": "x2 + 10"},
            "stroke": {"value": "#000"},
            "strokeWidth": {"value": 1.5},
            "strokeDash": {"value": [8,8]}
          },
          "update": {
            "y": {"scale": "y", "signal": "upper_signal"}
          }
        }
      },
      {
        "type": "text",
        "encode":{
          "update": {
            "text": {"value": "hey"},
            "baseline": {"value": "middle"},
            "x":{"signal": "x2 + 20"},
            "y": {"scale": "y", "signal": "upper_annot"},
            "fontSize": {"value": 14}
          }
        }
      }
    ]
  }
  return spec
