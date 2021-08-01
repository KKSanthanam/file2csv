#!/usr/bin/env python3
import apache_beam as beam
import apache_beam.transforms.window as window
from apache_beam.options.pipeline_options import PipelineOptions
from file2csv.Converter import Converter



def run_pipeline(fixedfile: str, specfile: str, csvfile: str) -> bool:
  converter = Converter(fixedfile, csvfile, specfile)
  # Load pipeline options from the script's arguments
  options = PipelineOptions()
  # Create a pipeline and run it after leaving the 'with' block
  with beam.Pipeline(options=options) as p:
    # Wrap in paranthesis to avoid Python indention issues
    (p 
    # Load data from input file
    | 'Read Lines' >> beam.io.ReadFromText(fixedfile)
    | 'Conver to CSV' >> beam.Map(lambda line: converter.encode(line))
    )
    # # Wrap in paranthesis to avoid Python indention issues
    # (p
    #  # Load some dummy data, this can be replaced with a proper source later on
    #  | 'Create words' >> beam.Create('to be or not to be')
    #  # Split the words into one element per word
    #  | 'Split words' >> beam.FlatMap(lambda words: words.split(' ')
    #  # We are assigning a count of 1 to every word (very relevant if we had more data)
    #  | 'Pair with 1' >> beam.Map(lambda word: (word, 1))
    #  # We are interested in 10 second periods of words
    #  | 'Window of 10 seconds' >> beam.WindowInto(window.FixedWindows(10))
    #  # Group all the values (counts) of each unique word
    #  | 'Group by key' >> beam.GroupByKey()
    #  # Sum the counts for each word and return the result
    #  | 'Sum word counts' >> beam.Map(lambda kv: (kv[0], sum(kv[1])))
    #  # Just print to the console for testing
    #  | 'Print to console' >> beam.Map(lambda wordcount: print(wordcount))
    # ))


if __name__ == "__main__":
  run_pipeline('data/fixedfile.txt')
