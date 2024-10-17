library(shiny)
library(tidyverse)
library(tidygraph)
library(igraph)
# library(arrow)

# data = read_parquet("overgroud_edge.parquet")
data = readr::read_csv("overgroud_edge.csv") |> 
  janitor::clean_names() |> 
  select(-x1)

g = igraph::graph_from_data_frame(data)
g |> 
  as_tbl_graph() |> 
  mutate(label=name) |> 
  visNetwork::visIgraph(layout="layout_with_kk") |> 
  visNetwork::visNodes(shape="text", physics = T) |> 
  visNetwork::visSave("overground_net.html")

sample(V(g)$name,2)



ui <- fluidPage(
  
)

server <- function(input, output, session) {
  
}

shinyApp(ui, server)

