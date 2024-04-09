
class EventAnalyzer:
    @staticmethod
    def get_joiners_multiple_meetings_method(events):
        joiners_dict = {}
        for event in events:
            for joiner in event["joiners"]:  
                joiner_name = joiner["name"]  
                if joiner_name not in joiners_dict:
                    joiners_dict[joiner_name] = 1
                else:
                    joiners_dict[joiner_name] += 1
        
        return [joiner_name for joiner_name, meetings_attended in joiners_dict.items() if meetings_attended >=2]
