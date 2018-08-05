import Html exposing (beginnerProgram, div, button, text, input)
import Html.Attributes exposing (..)
import Html.Events exposing (onClick, onInput)

-- Model

type Msg = Generate | LengthChange String


type alias Model =
  { password : String
  , length : Int
  }


model : Model
model =
  Model "" 0

main =
  beginnerProgram { model = model, view = view, update = update }


-- View

view model =
  div []
    [ input [ placeholder "Number of characters", onInput LengthChange ] []
    , button [ onClick Generate ] [ text "Generate" ]
    , text model.password
    ]


generateRandomPassword = 
  "TODO"

-- Update

update msg model =
  case msg of 
    Generate ->
      { model | password = generateRandomPassword }
    
    LengthChange len -> 
      { model | length = Result.withDefault 8 (String.toInt len) }
