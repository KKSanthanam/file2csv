#!/usr/bin/env python3
import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from file2csv.Converter import Converter


def run_pipeline(fixedfile: str, specfile: str, csvfile: str) -> bool:
  converter = Converter(specfile=specfile)
  # Load pipeline options from the script's arguments
  options = PipelineOptions()
  # Create a pipeline and run it after leaving the 'with' block
  with beam.Pipeline(options=options) as p:
    # Wrap in paranthesis to avoid Python indention issues
    (p 
    # Load data from input file
    | 'Read Lines' >> beam.io.ReadFromText(fixedfile)
    # convert to encoded value
    | 'Convert to CSV' >> beam.Map(lambda line: converter.encode(line))
    # Filter out the False record
    | 'Filter out False' >> beam.Filter(lambda pair: pair[0])
    # extract just line
    | 'Extract for CSV' >> beam.Map(lambda pair: pair[1])
    # Write to CSV
    | 'Write to CSV File' >> beam.io.WriteToText(csvfile, num_shards=3)
    )

if __name__ == "__main__":
  run_pipeline('data/fixedfile.txt', 'data/specfile.json', 'data/delimitfile.csv')
