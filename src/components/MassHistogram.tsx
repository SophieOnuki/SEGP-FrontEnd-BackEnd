import React, { useEffect, useRef } from 'react';
import Plotly from 'plotly.js-dist-min';

interface MassHistogramProps {
  masses: number[];
}

const MassHistogram: React.FC<MassHistogramProps> = ({ masses }) => {
  const chartRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!chartRef.current || masses.length === 0) return;

    const mean = masses.reduce((a, b) => a + b, 0) / masses.length;
    const variance = masses.reduce((acc, m) => acc + Math.pow(m - mean, 2), 0) / masses.length;
    const std = Math.sqrt(variance);

    const minMass = Math.min(...masses);
    const maxMass = Math.max(...masses);
    const step = (maxMass - minMass) / 100;
    const xVals: number[] = [];
    const yVals: number[] = [];
    for (let x = minMass; x <= maxMass; x += step) {
      const exponent = -Math.pow(x - mean, 2) / (2 * Math.pow(std, 2));
      const y = (1 / (std * Math.sqrt(2 * Math.PI))) * Math.exp(exponent);
      xVals.push(x);
      yVals.push(y);
    }

    const histTrace: Plotly.Data = {
      x: masses,
      type: 'histogram',
      histnorm: 'probability density',
      name: 'Observed masses',
      marker: { color: '#2c7fb8', line: { color: 'white', width: 1 } },
      opacity: 0.7,
    };

    const gaussTrace: Plotly.Data = {
      x: xVals,
      y: yVals,
      type: 'scatter',
      mode: 'lines',
      name: `Gaussian (μ=${mean.toFixed(2)} kg, σ=${std.toFixed(2)} kg)`,
      line: { color: '#d9534f', width: 2 },
    };

    const layout: Partial<Plotly.Layout> = {
      title: 'FFB Mass Distribution per Frame',
      xaxis: {
        title: { text: 'Mass (kg)', font: { size: 14, weight: 'bold' } },
        gridcolor: '#eee',
        zeroline: false,
      },
      yaxis: {
        title: { text: 'Probability Density', font: { size: 14, weight: 'bold' } },
        gridcolor: '#eee',
        zeroline: false,
      },
      bargap: 0.05,
      legend: { x: 0.7, y: 0.95, bgcolor: 'rgba(255,255,255,0.8)' },
      hovermode: 'closest',
      margin: { t: 50, l: 70, r: 30, b: 60 },
    };

    Plotly.newPlot(chartRef.current, [histTrace, gaussTrace], layout, { responsive: true });
  }, [masses]);

  if (masses.length === 0) {
    return <p style={{ textAlign: 'center', color: '#666' }}>No frame mass data available.</p>;
  }

  return <div ref={chartRef} style={{ width: '100%', height: '500px' }} />;
};

export default MassHistogram;