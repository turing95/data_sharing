
from django.shortcuts import render
import json
from django.http import HttpResponse

def walkthrough_tipbox(request):
    sequence_name = request.GET.get('sequence')
    step = request.GET.get('step')
    
    # Load the sequences from the JSON file
    with open('config/walkthrough_sequences.json') as json_file:
        sequences = json.load(json_file)
    
    # Access the requested sequence
    sequence = sequences.get(sequence_name)
    if sequence:
        # Convert step to an integer for arithmetic operations
        step_number = int(step)
        
        # Access the requested step
        step_data = sequence.get(step)
        if step_data:
            # Calculate next and previous step numbers
            next_step_number = step_number + 1
            prev_step_number = step_number - 1
            
            # Check the existence of the next and previous steps
            next_step_exists = str(next_step_number) in sequence
            prev_step_exists = str(prev_step_number) in sequence
            
            # Prepare the context for the template
            context = {
                'sequence': sequence_name,
                'content': step_data['content'],
                'target': step_data['target'],
                'next_step': str(next_step_number) if next_step_exists else None,
                'prev_step': str(prev_step_number) if prev_step_exists else None,
                'step': step_number+1,
                'tot_steps': len(sequence),
            }
            
            # Render the template with the context
            return render(request, 'components/walkthrough_tipbox.html', context)
    
    # If the requested sequence or step is not found, handle it
    return HttpResponse("Sequence or step not found", status=404)
    

    