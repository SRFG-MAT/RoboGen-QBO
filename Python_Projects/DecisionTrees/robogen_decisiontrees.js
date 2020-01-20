module.exports = {

	"SLE": {
		"id": "SLE",
		"question": "Es scheint als hättest du in letzter Zeit schlecht geschlafen. Kann es sein, dass du dich müde fühlst?",
		"options": [
			{
				"id": "SLE-opt-1",
				"question": "Ja, ich fühle mich müde und hätte gerne einen Tipp dazu.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": "STR_Sleep"
				}
			},
			{
				"id": "SLE-opt-2",
				"question": "Nein, ich fühle mich nicht müde.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": "EX_TL_Supporting_Message"
				}
			}
		]
	},
	"GAM": {
		"id": "GAM",
		"question": "Hast du Lust auf ein Spiel?",
		"options": [
			{
				"id": "GAM-opt-1",
				"question": "Ja, ich würde gerne ein Spiel spielen.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": "GAM_General"
				}
			},
			{
				"id": "GAM-opt-2",
				"question": "Nein, gerade nicht.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": "EX_TL_Supporting_Message"
				}
			}
		]
	},
	"EX": {
		"id": "EX",
		"question": "Dir machen Sport und Bewegung Probleme? Schau mal, ob dir eines von diesen Problemen bekannt vorkommt.",
		"options": [
			{
				"id": "EX-opt-1",
				"question": "Ich mache zu wenig Bewegung / Sport.",
				"condition": "",
				"action": {
					"type": "SUBTREE",
					"ref": "EX-1"
				}
			},
			{
				"id": "EX-opt-2",
				"question": "Ich mache Bewegung / Sport so wie ich es soll, bin aber nicht glücklich damit.",
				"condition": "",
				"action": {
					"type": "SUBTREE",
					"ref": "EX-2"
				}
			},
			{
				"id": "EX-opt-3",
				"question": "Ich mache zu viel Bewegung / Sport.",
				"condition": "",
				"action": {
					"type": "SUBTREE",
					"ref": "EX-3"
				}
			}
		]
	},
	"EX-1": {
		"id": "EX-1",
		"question": "Könnte eines der folgenden Themen der Grund für zu wenig Bewegung / Sport sein?",
		"options": [
			{
				"id": "EX-1-opt-1",
				"question": "Ich habe Angst vor einer Unterzuckerung.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_Fear_Hypos"]
				}
			},
			{
				"id": "EX-1-opt-2",
				"question": "Ich möchte nicht, dass andere über meinen Diabetes Bescheid wissen.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_Fear_Disclosure_Process"]
				}
			},
			{
				"id": "EX-1-opt-3",
				"question": "Ich bin zu beschäftigt oder habe keine Zeit, um mich zu bewegen.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_Conflicting_Life_Goals"]
				}
			},
			{
				"id": "EX-1-opt-4",
				"question": "Ich mag keinen Sport.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_Negative_Affect_Process"]
				}
			},
			{
				"id": "EX-1-opt-5",
				"question": "Ich vergesse immer wieder meinen Sport zu machen.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_Forgetting_Process"]
				}
			},
			{
				"id": "EX-1-opt-6",
				"question": "Ich fühle mich in zu schlechter Stimmung, um Sport zu machen.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Depression","EX_TL_D_Depression"]
				}
			},
			{
				"id": "EX-1-opt-7",
				"question": "Ich fühle mich in zu schlechter Stimmung, um Sport zu machen.",
				"condition": "diabetes=false",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Depression"]
				}
			},
			{
				"id": "EX-1-opt-8",
				"question": "Von diesen Gründen trifft nichts zu",
				"condition": "",
				"action": {
					"type": "SUBTREE",
					"ref": "EX-1-1"
				}
			}
		]
	},
	"EX-2": {
		"id": "EX-2",
		"question": "Könnte eines der folgenden Themen der Grund dafür sein, dass du mit deiner Bewegung / Sport nicht glücklich bist?",
		"options": [
			{
				"id": "EX-2-opt-1",
				"question": "Ich möchte nicht, dass andere über meinen Diabetes Bescheid wissen.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_Fear_Disclosure_Process"]
				}
			},
			{
				"id": "EX-2-opt-2",
				"question": "Sport und Bewegung wirken sich nicht auf meinen Diabetes aus.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_General_Importance"]
				}
			},
			{
				"id": "EX-2-opt-3",
				"question": "Ich mag keinen Sport.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_Negative_Affect_Process"]
				}
			},
			{
				"id": "EX-2-opt-4",
				"question": "Ich fühle mich schlecht, wenn ich Sport mache.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Depression","EX_TL_D_Depression"]
				}
			},
			{
				"id": "EX-2-opt-5",
				"question": "Ich fühle mich schlecht, wenn ich Sport mache.",
				"condition": "diabetes=false",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Depression"]
				}
			},
			{
				"id": "EX-2-opt-6",
				"question": "Von diesen Gründen trifft nichts zu.",
				"condition": "",
				"action": {
					"type": "SUBTREE",
					"ref": "EX-2-1"
				}
			}
		]
	},
	"EX-3": {
		"id": "EX-3",
		"question": "Könnte eines der folgenden Themen der Grund für zu viel Bewegung / Sport sein?",
		"options": [
			{
				"id": "EX-3-opt-1",
				"question": "Ich habe Angst vor Komplikationen, weil meine Glukose-Wert zu hoch ist.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TM_D_Fear_Complications"]
				}
			},
			{
				"id": "EX-3-opt-2",
				"question": "Nichts davon trifft zu.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Supporting_Message"]
				}
			}
		]
	},
	"EX-1-1": {
		"id": "EX-1-1",
		"question": "Wie wäre es damit?",
		"options": [
			{
				"id": "EX-1-1-opt-1",
				"question": "Ich werde mein Ziel niemals erreichen, egal wie sehr ich es versuche.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Motivation_Process","EX_TL_D_Motivation_Process"]
				}
			},
			{
				"id": "EX-1-1-opt-2",
				"question": "Ich werde mein Ziel niemals erreichen, egal wie sehr ich es versuche.",
				"condition": "diabetes=false",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Motivation_Process"]
				}
			},
			{
				"id": "EX-1-1-opt-3",
				"question": "Ich fühle mich mit Diabetes unwohl in der Öffentlichkeit.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_Fear_Disclosure_Process"]
				}
			},
			{
				"id": "EX-1-1-opt-4",
				"question": "Sport und Bewegung sind mir nicht wichtig.",
				"condition": "diabetes=false",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Personal_Importance"]
				}
			},
			{
				"id": "EX-1-1-opt-5",
				"question": "Sport und Bewegung sind mir nicht wichtig.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_D_General_Importance"]
				}
			},
			{
				"id": "EX-1-1-opt-6",
				"question": "Nichts davon trifft zu.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Supporting_Message"]
				}
			}
		]
	},
	"EX-2-1": {
		"id": "EX-2-1",
		"question": "Wie wäre es damit?",
		"options": [
			{
				"id": "EX-2-1-opt-1",
				"question": "Ich interessiere mich nicht wirklich für Sport.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_OK_Personal_Importance"]
				}
			},
			{
				"id": "EX-2-1-opt-2",
				"question": "Nichts davon trifft zu.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["EX_TL_Supporting_Message"]
				}
			}
		]
	},
	"STR": {
		"id": "STR",
		"question": "Du fühlst dich immer wieder gestresst und möchtest dir gerne anschauen warum das so ist? Möchtest du gerne erfahren, wie du deinem Stress auf die Spur kommst?",
		"options": [
			{
				"id": "STR-opt-1",
				"question": "Ich bin immer zu beschäftigt und das stresst mich.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_D_Goal_Conflict"]
				}
			},
			{
				"id": "STR-opt-2",
				"question": "Meine negative Stimmung verursacht mir Stress.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_D_Negative_Affect"]
				}
			},
			{
				"id": "STR-opt-3",
				"question": "Meine negative Stimmung verursacht mir Stress.",
				"condition": "diabetes=false",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Negative_Affect"]
				}
			},
			{
				"id": "STR-opt-4",
				"question": "Ich fühle mich einsam und alleine.",
				"condition": "age>=60",
				"action": {
					"type": "INTERVENTION",
					"ref": ["SEN_Einsam"]
				}
			},
			{
				"id": "STR-opt-5",
				"question": "Mir fehlt jetzt in der Pension eine sinnvolle Aufgabe oder Beschäftigung.",
				"condition": "age>=60",
				"action": {
					"type": "INTERVENTION",
					"ref": ["SEN_Pension"]
				}
			},
			{
				"id": "STR-opt-6",
				"question": "Ich gerate in Stress, wenn sich Alltagsabläufe bzw. Routinetätigkeiten ungeplant verändern.",
				"condition": "age>=60",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Zeitmanagement","SEN_Zeitmanagement_Senior"]
				}
			},
			{
				"id": "STR-opt-7",
				"question": "Häufige Schmerzen sind eine Ursache für meinen Stress.",
				"condition": "age>=60",
				"action": {
					"type": "INTERVENTION",
					"ref": ["SEN_Pain"]
				}
			},
			{
				"id": "STR-opt-8",
				"question": "Ich möchte mir anschauen bei welchen Gelegenheiten ich in Stress gerate.",
				"condition": "",
				"action": {
					"type": "SUBTREE",
					"ref": "STR-1"
				}
			},
			{
				"id": "STR-opt-9",
				"question": "Ich möchte mir anschauen was ich selber zu meinem Stress beitrage.",
				"condition": "",
				"action": {
					"type": "SUBTREE",
					"ref": "STR-2"
				}
			},
			{
				"id": "STR-opt-10",
				"question": "Ich möchte mir anschauen wie sich Stress bei mir auswirkt.",
				"condition": "",
				"action": {
					"type": "SUBTREE",
					"ref": "STR-3"
				}
			},
			{
				"id": "STR-opt-11",
				"question": "Ich möchte mir anschauen wie ich meinen Stress besser in den Griff bekomme.",
				"condition": "",
				"action": {
					"type": "SUBTREE",
					"ref": "STR-4"
				}
			},
			{
				"id": "STR-opt-12",
				"question": "Ich fühle mich gestresst und weiß nicht warum.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_D_General"]
				}
			},
			{
				"id": "STR-opt-13",
				"question": "Ich fühle mich gestresst und weiß nicht warum.",
				"condition": "diabetes=false",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_General","STR_Goal_Conflict"]
				}
			}
		]
	},
	"STR-1": {
		"id": "STR-1",
		"question": "Gerätst du bei einem der folgenden Themen in Stress?",
		"options": [
			{
				"id": "STR-1-opt-1",
				"question": "Ich möchte verstehen, wodurch Stress verursacht werden kann.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Stressoren"]
				}
			},
			{
				"id": "STR-1-opt-2",
				"question": "Ich gerate in Stress, wenn keine Zeit für eine Pause ist.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Zeitmanagement","STR_Pause"]
				}
			},
			{
				"id": "STR-1-opt-3",
				"question": "Ich gerate in Stress, wenn zu viel Arbeit gleichzeitig erledigt werden muss.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Zeitmanagement"]
				}
			},
			{
				"id": "STR-1-opt-4",
				"question": "Ich gerate in Stress, wenn ich ständig unterbrochen werde.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Zeitmanagement"]
				}
			},
			{
				"id": "STR-1-opt-5",
				"question": "Ich gerate in Stress, weiß aber nicht genau wieso.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Stressoren_Coping"]
				}
			}
		]
	},
	"STR-2": {
		"id": "STR-2",
		"question": "Trifft eine der folgenden Aussagen auf dich zu?",
		"options": [
			{
				"id": "STR-2-opt-1",
				"question": "Ich muss immer alles richtig machen. Auf mich muss 100% Verlass sein.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Sei-perfekt"]
				}
			},
			{
				"id": "STR-2-opt-2",
				"question": "Ich will mit allen Leuten gut auskommen.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Sei-beliebt"]
				}
			},
			{
				"id": "STR-2-opt-3",
				"question": "Am liebsten mache ich alles selber.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Sei-stark"]
				}
			},
			{
				"id": "STR-2-opt-4",
				"question": "Es ist mir wichtig, dass ich alles unter Kontrolle habe.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Sei-vorsichtig"]
				}
			},
			{
				"id": "STR-2-opt-5",
				"question": "Ich halte das nicht durch. Ich werde versagen.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Ich-kann-nicht"]
				}
			},
			{
				"id": "STR-2-opt-6",
				"question": "Ich nehme mir oft zu viel vor.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Realitätstestung"]
				}
			},
			{
				"id": "STR-2-opt-7",
				"question": "Ich fühle mich durch das Verhalten von Anderen oder durch äußere Situationen persönlich betroffen.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Relativieren"]
				}
			},
			{
				"id": "STR-2-opt-8",
				"question": "Ich male mir oft aus welche schlimmen Konsequenzen ein mögliches Versagen haben könnte.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Entkastrophieren"]
				}
			}
		]
	},
	"STR-3": {
		"id": "STR-3",
		"question": "Interessierst du dich für eines der folgenden Themen?",
		"options": [
			{
				"id": "STR-3-opt-1",
				"question": "Ich möchte verstehen wie Stress sich bei mir auswirken kann.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Stressreaktionen"]
				}
			},
			{
				"id": "STR-3-opt-2",
				"question": "Ich möchte mir Methoden anschauen, um Stress abzubauen.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Entspannung"]
				}
			}
		]
	},
	"STR-4": {
		"id": "STR-4",
		"question": "Trifft eine der folgenden Aussagen auf dich zu?",
		"options": [
			{
				"id": "STR-4-opt-1",
				"question": "Ich fühle mich müde / erschöpft und habe wenig Energie für meine alltäglichen Aktivitäten.",
				"condition": "",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_Goal_Conflict"]
				}
			},
			{
				"id": "STR-4-opt-2",
				"question": "Ich fühle mich gestresst und weiß nicht warum.",
				"condition": "diabetes=true",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_D_General"]
				}
			},
			{
				"id": "STR-4-opt-3",
				"question": "Ich fühle mich gestresst und weiß nicht warum.",
				"condition": "diabetes=false",
				"action": {
					"type": "INTERVENTION",
					"ref": ["STR_General","STR_Goal_Conflict"]
				}
			}
		]
	}

};