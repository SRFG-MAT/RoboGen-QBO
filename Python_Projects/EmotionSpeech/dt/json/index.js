"use strict";
const Alexa = require('alexa-sdk');
const APP_ID = undefined;

let calledInAndroidMode = false;
let speechOutput = '';
let welcomeReprompt = '';
let reprompt;

let welcome_1 = "Willkommen im RoboGen Entscheidungsbaum.";
let welcome_2 = "Damit ich dir die richtigen Themen anzeige, muss ich dir zwei kurze Fragen stellen. Möchtest du Themen behandeln, die auf Diabetes eingehen?";
let welcome_3 = "Danke, das merke ich mir. Möchtest du Themen behandeln, die auf SeniorenInnen eingehen?";
let welcome_4 = "In Ordnung. Nun weiß ich welche Themen ich dir anzeigen werde.";
let welcome_5 = "Wähle nun den Entscheidungsbaum Sport, Stress, Schlaf oder Spiele, um fortzufahren.";
let cancel = "Danke fürs Mitmachen! Auf Wiedersehen!";
let stop = "Schließe aktuellen Entscheidungsbaum. Du kannst jetzt einen anderen Baum wählen!";
let error = "Diese Antwort ist im Moment nicht möglich. Bitte sieh dir die letzte Frage nochmal genau an!";
let internal_error = "Hier ist wohl etwas schiefgegangen - tut mir leid. Sage 'Stop', um zur Auswahl zurückzukehren oder 'Verlassen', um die Anwendung zu beenden.";
let help = "Derzeit werden die Entscheidungsbäume Sport, Stress, Schlaf und Spiele unterstützt. Sag einfach eines dieser Schlüsselwörter um einen Entscheidungsbaum zu starten!";
let remove = "Alle gespeicherten Informationen wurden gelöscht!";
let additional = "Zu diesem Thema gibt es weiterführende Links. Sage 'Thema merken', um diese später in der RoboGen App aufrufen zu können."; 
let additional_approve = "In Ordnung. Dieses Thema kann nun in der RoboGen App aufgerufen werden.";
let fin = "Dies ist das Ende des aktuellen Entscheidungsbaums. Sage 'Stop', um zur Auswahl zurückzukehren oder 'Verlassen', um die Anwendung zu beenden.";

const display = require('./display.js');
const helpers = require('./helpers.js');

const dts = require('./robogen_decisiontrees.js');
const interventions = require('./robogen_interventions.js');

var dataUserInfos = require('./saved_data/data_user.json');
var dataStateMachine = require('./saved_data/data_state.json');

const handlers = {
	
	'LaunchRequest': function () {
		this.emit(':loadState', true);
		if (dataStateMachine.introComplete) {
			speechOutput = welcome_1 + " " + welcome_5;
			helpers.output_EmitandDisplay(this, display, speechOutput, speechOutput, welcomeReprompt, "INT");
		}
		else {
			dataStateMachine.lastSelection = "welcome_2";
			speechOutput = welcome_1 + " " + welcome_2;
			helpers.output_EmitandDisplay(this, display, speechOutput, speechOutput, welcomeReprompt, "INT");
		}
	},
	
    'SessionEndedRequest': function () {
    	helpers.resetStateMachine(dataStateMachine);
		helpers.output_EmitandDisplay(this, display, cancel, cancel, welcomeReprompt, "INT");
		this.emit(':saveState', true);
    },
	
    'Nutzerdaten_Entfernen': function () {
    	helpers.resetUserData(dataUserInfos);
    	speechOutput = outputs.getOutputString_DeleteUserData();
    	helpers.output_EmitandDisplay(this, display, remove, remove, welcomeReprompt, "INT");
    },
	
	'Entscheidungsbaum_Stress': function () {
		dataStateMachine.lastSelection = "STR";
		this.emit('Subtree');
	},
	
	'Entscheidungsbaum_Sport': function () {
		dataStateMachine.lastSelection = "EX";
		this.emit('Subtree');
    },
	
	'Entscheidungsbaum_Schlaf': function() {
		dataStateMachine.lastSelection = "SLE";
		this.emit('Subtree');
	},
	
	'Entscheidungsbaum_Spiele': function() {
		dataStateMachine.lastSelection = "GAM";
		this.emit('Subtree');
	},
	
	'Subtree': function () {
		if (dataStateMachine.lastSelection != "") {
			dataStateMachine.selectedPath.push(dataStateMachine.lastSelection);
			if (dts[dataStateMachine.lastSelection]) {
				let tree = dts[dataStateMachine.lastSelection];
				dataStateMachine.lastSelection = "";
				dataStateMachine.lastInterventions = [];
				dataStateMachine.lastOptions = [];
				let validOptions = [];
				for (let i=0; i<tree.options.length; i++) {
					let opt = tree.options[i];
					if (opt.condition == "") {
						validOptions.push(opt);
					}
					else if (opt.condition == "diabetes=true" && dataUserInfos.showDiabetes) {
						validOptions.push(opt);
					}
					else if (opt.condition == "diabetes=false" && !dataUserInfos.showDiabetes) {
						validOptions.push(opt);
					}
					else if (opt.condition == "age>=60" && dataUserInfos.showSenior) {
						validOptions.push(opt);
					}
				}
				if (validOptions.length > 0) {
					dataStateMachine.lastOptions = validOptions;
					speechOutput = tree.question + "\r\n";
					for (let i=0; i<dataStateMachine.lastOptions.length; i++) {
						speechOutput += "Antwort "+(i+1)+": "+dataStateMachine.lastOptions[i].question+"\r\n";
					}
					helpers.output_EmitandDisplay(this, display, speechOutput, speechOutput, welcomeReprompt, dataStateMachine.selectedPath[0]);
				}
				else {
					helpers.output_EmitandDisplay(this, display, internal_error, internal_error, welcomeReprompt, "ERR");
				}
			}
			else {
				helpers.output_EmitandDisplay(this, display, internal_error, internal_error, welcomeReprompt, "ERR");
			}
		}
		else {
			helpers.output_EmitandDisplay(this, display, internal_error, internal_error, welcomeReprompt, "ERR");
		}
	},
	
	'Intervention': function () {
		if (dataStateMachine.lastInterventions.length > 0) {
			let selInt = dataStateMachine.lastInterventions;
			dataStateMachine.lastSelection = "";
			dataStateMachine.lastInterventions = [];
			dataStateMachine.lastOptions = [];
			let validInterventions = [];
			for (let i=0; i<interventions.length; i++) {
				let valid = false;
				for (let j=0; j<interventions[i].codes.length; j++) {
					let code = interventions[i].codes[j];
					if (selInt.indexOf(code) != -1) {
						valid = true;
					}
				}
				if (valid) {
					validInterventions.push(interventions[i]);
				}
			}
			if (validInterventions.length > 0) {
				let chosenInt = validInterventions[Math.floor(Math.random()*validInterventions.length)];
				dataUserInfos.selectedPath = dataStateMachine.selectedPath;
				dataUserInfos.shownIntervention = chosenInt.text;
				dataUserInfos.shownInterventions.push({
					"selectedPath": dataStateMachine.selectedPath,
					"shownIntervention": chosenInt.text,
					"additionalLink": chosenInt.link,
					"remember": false
				});
				speechOutput = chosenInt.text;
				if (chosenInt.link != "") {
					speechOutput += " " + additional;
				}
				speechOutput += "\r\n" + fin;
				helpers.output_EmitandDisplay(this, display, speechOutput, speechOutput, welcomeReprompt, dataStateMachine.selectedPath[0]);
			}
			else {
				helpers.output_EmitandDisplay(this, display, internal_error, internal_error, welcomeReprompt, "ERR");
			}
		}
		else {
			helpers.output_EmitandDisplay(this, display, internal_error, internal_error, welcomeReprompt, "ERR");
		}
	},
	
	'Thema_Merken': function() {
		if (dataStateMachine.lastSelection == "" && dataUserInfos.shownInterventions.length >0 && !dataUserInfos.shownInterventions[dataUserInfos.shownInterventions.length-1].remember) {
			dataUserInfos.shownInterventions[dataUserInfos.shownInterventions.length-1].remember = true;
			speechOutput = additional_approve + "\r\n" + fin;
			helpers.output_EmitandDisplay(this, display, speechOutput, speechOutput, welcomeReprompt, dataStateMachine.selectedPath[0]);
		}
		else {
			helpers.output_EmitandDisplay(this, display, internal_error, internal_error, welcomeReprompt, "ERR");
		}
	},
	
	'ElementSelected': function() {
		this.emit('Option_X',parseInt(this.event.request.token));
	},
	
    'Option_X': function (selIdx) {
		if (dataStateMachine.lastOptions.length > 0) {
			let idx = 0;
			if (selIdx) {
				idx = selIdx - 1;
			}
			else {
				idx = this.event.request.intent.slots.number.value - 1;
			}
			if (idx < dataStateMachine.lastOptions.length) {
				let opt = dataStateMachine.lastOptions[idx];
				if (opt.action && opt.action.type && (opt.action.type == "SUBTREE" || opt.action.type == "INTERVENTION")) {
					if (opt.action.type == "SUBTREE") {
						dataStateMachine.lastSelection = opt.action.ref;
						this.emit('Subtree');
					}
					else if (opt.action.type == "INTERVENTION") {
						dataStateMachine.lastInterventions = opt.action.ref;
						this.emit('Intervention');
					}
				}
				else {
					helpers.output_EmitandDisplay(this, display, internal_error, internal_error, welcomeReprompt, "ERR");
				}
			}
			else {
				this.emit(':ask', error, error);
			}
		}
		else {
			this.emit(':ask', error, error);
		}
    },
	
	'Fallback': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.FallbackIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.YesIntent': function () {
		if (dataStateMachine.lastSelection == "welcome_2") {
			dataUserInfos.showDiabetes = true;
			dataStateMachine.lastSelection = "welcome_3";
			helpers.output_EmitandDisplay(this, display, welcome_3, welcome_3, welcomeReprompt, "INT");
		}
		else if (dataStateMachine.lastSelection == "welcome_3") {
			dataUserInfos.showSenior = true;
			dataStateMachine.lastSelection = "";
			dataStateMachine.introComplete = true;
			speechOutput = welcome_4 + " " + welcome_5;
			helpers.output_EmitandDisplay(this, display, speechOutput, speechOutput, welcomeReprompt, "INT");
		}
		else {
			this.emit(':ask', error, error);
		}
    },
	
	'AMAZON.NoIntent': function () {
		if (dataStateMachine.lastSelection == "welcome_2") {
			dataUserInfos.showDiabetes = false;
			dataStateMachine.lastSelection = "welcome_3";
			helpers.output_EmitandDisplay(this, display, welcome_3, welcome_3, welcomeReprompt, "INT");
		}
		else if (dataStateMachine.lastSelection == "welcome_3") {
			dataUserInfos.showSenior = false;
			dataStateMachine.lastSelection = "";
			dataStateMachine.introComplete = true;
			speechOutput = welcome_4 + " " + welcome_5;
			helpers.output_EmitandDisplay(this, display, speechOutput, speechOutput, welcomeReprompt, "INT");
		}
		else {
			this.emit(':ask', error, error);
		}
    },
	
	'AMAZON.HelpIntent': function () {
		this.emit(':ask', help, help);
	},
	
    'AMAZON.CancelIntent': function () {
    	helpers.resetStateMachine(dataStateMachine);
		this.emit(':tell', cancel);
		this.close();
	},
	
	'AMAZON.StopIntent': function () {
		helpers.softResetStateMachine(dataStateMachine);
		this.emit('LaunchRequest');
	},
	
	'AMAZON.NavigateHomeIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.PauseIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.ResumeIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.MoreIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.NavigateSettingsIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.NextIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.PageUpIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.PageDownIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.PreviousIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.ScrollRightIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.ScrollDownIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.ScrollLeftIntent': function () {
		this.emit(':ask', error, error);
    },
	
	'AMAZON.ScrollUpIntent': function () {
		this.emit(':ask', error, error);
    },	
	
	'Unhandled': function () {
        this.emit(':ask', error, error);
    }
	
};

exports.handler = (event, context, callback) => {
	
	if (event.firstName == "Android" && event.lastName == "RoboGen") {
		calledInAndroidMode = true;
    	context.succeed(dataUserInfos);
	}
	else {
		calledInAndroidMode = false;
    	const alexa = Alexa.handler(event, context);
    	alexa.appId = APP_ID;
    	alexa.registerHandlers(handlers);
    	alexa.execute();
	}
	
};