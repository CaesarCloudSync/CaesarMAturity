if [[ $1 == "" ]]
then
  python -m unittest maturityunit.MaturityAssessmentCase
else
  python -m unittest maturityunit.MaturityAssessmentCase.$1
fi