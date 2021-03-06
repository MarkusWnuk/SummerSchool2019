/*
// Spring.cpp: Definiert den Einstiegspunkt für die Konsolenanwendung.
//

#include "stdafx.h"
#include <stdio.h>
#include "include\dhdc.h"

//#pragma comment(lib, "lib/dhdms.lib")

#define K   1000.0



// simple spring model which pulls the device
// towards the center of the workspace;
// if the user lifts the device 5cm above the center,
// the application exits
int
compute_my_forces(double px, double py, double pz,
	double *fx, double *fy, double *fz)
{
	// spring model
	*fx = -K * px;
	*fy = -K * py;
	*fz = -K * pz;

	// exit condition
	if (pz > 0.05) return 1;
	else           return 0;
}



int
main(int  argc,
	char **argv)
{
	int    done = 0;
	double px, py, pz;
	double fx, fy, fz;

	if (dhdOpen() < 0) {
		printf("error: cannot open device\n");
	}

	printf("spring model applied...\n");

	while (!done) {

		// get end-effector position
		dhdGetPosition(&px, &py, &pz);
		//sendPositionOut(px, py, pz);


		// compute force model
		done = compute_my_forces(px, py, pz, &fx, &fy, &fz);
		//printf("Position: %f, %f, %f, Forces:  %f, %f, %f\n", px, py, pz , fx, fy, fz);
		//printf("Forces: %f, %f, %f\n", fx, fy, fz);

		// apply forces
		//receiveForces(&fx, &fy, &fz);
		dhdSetForce(fx, fy, fz);

		// exit if the button is pushed
		done += dhdGetButton(0);
	}
	while (false)
	{
		printf("Position: %f, %f, %f, Forces:  %f, %f, %f\n", px, py, pz, fx, fy, fz);
		//
	}
	printf("exiting application\n");

	dhdClose();

	return 0;
}
*/


// async_subscribe.cpp
//
// This is a Paho MQTT C++ client, sample application.
//
// This application is an MQTT subscriber using the C++ asynchronous client
// interface, employing callbacks to receive messages and status updates.
//
// The sample demonstrates:
//  - Connecting to an MQTT server/broker.
//  - Subscribing to a topic
//  - Receiving messages through the callback API
//  - Receiving network disconnect updates and attempting manual reconnects.
//  - Using a "clean session" and manually re-subscribing to topics on
//    reconnect.
//

/*******************************************************************************
* Copyright (c) 2013-2017 Frank Pagliughi <fpagliughi@mindspring.com>
*
* All rights reserved. This program and the accompanying materials
* are made available under the terms of the Eclipse Public License v1.0
* and Eclipse Distribution License v1.0 which accompany this distribution.
*
* The Eclipse Public License is available at
*    http://www.eclipse.org/legal/epl-v10.html
* and the Eclipse Distribution License is available at
*   http://www.eclipse.org/org/documents/edl-v10.php.
*
* Contributors:
*    Frank Pagliughi - initial implementation and documentation
*******************************************************************************/

//header for haptic device
#include "stdafx.h"
#include <stdio.h>
#include "include\dhdc.h"
//header for mqtt client
#include <iostream>
#include <cstdlib>
#include <string>
#include <cstring>
#include <cctype>
#include <thread>
#include <chrono>
#include "mqtt/async_client.h"
#include "include/json.hpp"
using json = nlohmann::json;

double K = 1;
double px, py, pz;
double fx, fy, fz;
bool pushbutton;

json j_pos = "{ \"Px\": 0.0, \"Py\": 0.00, \"Pz\": 0.00 }"_json;
json j_but = "{ \"Button\": 0 }"_json;

const std::string SERVER_ADDRESS("tcp://192.169.1.3:1883");
const std::string CLIENT_ID("async_subcribe_cpp");
const std::string SUB_TOPIC("Sollwerte");
const std::string PUB_TOPIC("Pos_m");
const std::string PUB_TOPIC_BUTTON("SafetyButton");

const int	QOS = 0;
const int	N_RETRY_ATTEMPTS = 1;

/////////////////////////////////////////////////////////////////////////////

// Callbacks for the success or failures of requested actions.
// This could be used to initiate further action, but here we just log the
// results to the console.

class action_listener : public virtual mqtt::iaction_listener
{
	std::string name_;

	void on_failure(const mqtt::token& tok) override {
		std::cout << name_ << " failure";
		if (tok.get_message_id() != 0)
			std::cout << " for token: [" << tok.get_message_id() << "]" << std::endl;
		std::cout << std::endl;
	}

	void on_success(const mqtt::token& tok) override {
		std::cout << name_ << " success";
		if (tok.get_message_id() != 0)
			std::cout << " for token: [" << tok.get_message_id() << "]" << std::endl;
		auto top = tok.get_topics();
		if (top && !top->empty())
			std::cout << "\ttoken topic: '" << (*top)[0] << "', ..." << std::endl;
		std::cout << std::endl;
	}

public:
	action_listener(const std::string& name) : name_(name) {}
};

/////////////////////////////////////////////////////////////////////////////

/**
* Local callback & listener class for use with the client connection.
* This is primarily intended to receive messages, but it will also monitor
* the connection to the broker. If the connection is lost, it will attempt
* to restore the connection and re-subscribe to the topic.
*/
class callback : public virtual mqtt::callback,
	public virtual mqtt::iaction_listener

{
	// Counter for the number of connection retries
	int nretry_;
	// The MQTT client
	mqtt::async_client& cli_;
	// Options to use if we need to reconnect
	mqtt::connect_options& connOpts_;
	// An action listener to display the result of actions.
	action_listener subListener_;

	// This deomonstrates manually reconnecting to the broker by calling
	// connect() again. This is a possibility for an application that keeps
	// a copy of it's original connect_options, or if the app wants to
	// reconnect with different options.
	// Another way this can be done manually, if using the same options, is
	// to just call the async_client::reconnect() method.
	void reconnect() {
		std::this_thread::sleep_for(std::chrono::milliseconds(2500));
		try {
			cli_.connect(connOpts_, nullptr, *this);
		}
		catch (const mqtt::exception& exc) {
			std::cerr << "Error: " << exc.what() << std::endl;
			exit(1);
		}
	}

	// Re-connection failure
	void on_failure(const mqtt::token& tok) override {
		std::cout << "Connection attempt failed" << std::endl;
		if (++nretry_ > N_RETRY_ATTEMPTS)
			exit(1);
		reconnect();
	}

	// (Re)connection success
	// Either this or connected() can be used for callbacks.
	void on_success(const mqtt::token& tok) override {}

	// (Re)connection success
	void connected(const std::string& cause) override {
		std::cout << "\nConnection success" << std::endl;
		std::cout << "\nSubscribing to topic '" << SUB_TOPIC << "'\n"
			<< "\tfor client " << CLIENT_ID
			<< " using QoS" << QOS << "\n"
			<< "\nPress Q<Enter> to quit\n" << std::endl;

		cli_.subscribe(SUB_TOPIC, QOS, nullptr, subListener_);
	}

	// Callback for when the connection is lost.
	// This will initiate the attempt to manually reconnect.
	void connection_lost(const std::string& cause) override {
		std::cout << "\nConnection lost" << std::endl;
		if (!cause.empty())
			std::cout << "\tcause: " << cause << std::endl;

		std::cout << "Reconnecting..." << std::endl;
		nretry_ = 0;
		reconnect();
	}

	// Callback for when a message arrives.
	void message_arrived(mqtt::const_message_ptr msg) override {
		bool printout = false;
		if (printout)
		{
		std::cout << "Message arrived" << std::endl;
		std::cout << "\ttopic: '" << msg->get_topic() << "'" << std::endl;
		std::cout << "\tpayload: '" << msg->to_string() << "'\n" << std::endl;
		}

		//Assume the topic and message are always correct

		try
		{
			auto j_f = json::parse(msg->to_string());
			double jfx = j_f["Fx"];
			double jfy = j_f["Fy"];
			double jfz = j_f["Fz"];

			//limit Force Values
			double max_force = 2;
			fx = ((jfx) > 40) ? max_force : jfx;
			fx = ((jfx) < -40) ? -max_force : jfx;


			fy = ((jfy) > 40) ? max_force : jfy;
			fy = ((jfy) < -40) ? -max_force : jfy;


			fz = ((jfz) > 40) ? max_force : jfz;
			fz = ((jfz) < -40) ? -max_force : jfz;


			if (printout)
			{
			printf("received Forces:  %f, %f, %f\n", jfx, jfy, jfz);
			}
			else
			{
			//printf("A");
			}
		}
		catch (const std::exception&)
		{
			printf("error Forces");
			std::cout << msg->to_string() << std::endl;

		}
		

	}

	void delivery_complete(mqtt::delivery_token_ptr token) override {}

public:
	callback(mqtt::async_client& cli, mqtt::connect_options& connOpts)
		: nretry_(0), cli_(cli), connOpts_(connOpts), subListener_("Subscription") {}
};

/////////////////////////////////////////////////////////////////////////////

int main(int argc, char* argv[])
{
	using namespace std::this_thread; // sleep_for, sleep_until
	using namespace std::chrono; // nanoseconds, system_clock, seconds


	mqtt::connect_options connOpts;
	connOpts.set_keep_alive_interval(20);
	connOpts.set_clean_session(true);
	//connOpts.set_user_name("summer2019");
	//connOpts.set_password("softtissue");

	mqtt::async_client client(SERVER_ADDRESS, CLIENT_ID);

	callback cb(client, connOpts);
	client.set_callback(cb);

	// Start the connection.
	// When completed, the callback will subscribe to topic.

	try {
		std::cout << "Connecting to the MQTT server..." << std::flush;
		client.connect(connOpts, nullptr, cb);
	}
	catch (const mqtt::exception&) {
		std::cerr << "\nERROR: Unable to connect to MQTT server: '"
			<< SERVER_ADDRESS << "'" << std::endl;
		return 1;
	}

	// Just block till user tells us to quit.

	//loop for haptic device
	int    done = 0;

	if (dhdOpen() < 0) {
		printf("error: cannot open device\n");
	}

	printf("spring model applied...\n");
	fx = 0;
	fy = 0;
	fz = 0;
	while (!done) {

		// get end-effector position
		dhdGetPosition(&px, &py, &pz);
		//sendPositionOut(px, py, pz);

		//get button status
		pushbutton = dhdGetButton(0);
		// compute force model
		//done = compute_my_forces(px, py, pz, &fx, &fy, &fz);
		//printf("Position: %f, %f, %f, Forces:  %f, %f, %f\n", px, py, pz , fx, fy, fz);
		//printf("Forces: %f, %f, %f\n", fx, fy, fz);

		// apply forces
		//receiveForces(&fx, &fy, &fz);
		dhdSetForce(fx, fy, fz);


		// exit if the button is pushed
		//done += dhdGetButton(0);

		bool send_positions = true;
		if (send_positions)
		{
			j_pos["Px"] = px;
			j_pos["Py"] = py;
			j_pos["Pz"] = pz;
			bool printoutSend = false;
			if (printoutSend)
			{
				std::cout << "\nSending message..." << std::endl;
			}
			mqtt::message_ptr pubmsg = mqtt::make_message(PUB_TOPIC, j_pos.dump());
			pubmsg->set_qos(QOS);
			if (printoutSend)
			{
				printf("measured positions:  %f, %f, %f\n", px, py, pz);
			}
			client.publish(pubmsg);// ->wait_for(TIMEOUT);
			sleep_for(milliseconds(8));
			if (printoutSend)
			{
				std::cout << "  ...OK" << std::endl;
			}
		}
		bool send_button = true;
		if (send_button)
		{
			j_but["Button"] = pushbutton;
			bool printoutSend = true;
			if (printoutSend)
			{
				std::cout << "\nSending message..." << std::endl;
			}
			mqtt::message_ptr pubmsg = mqtt::make_message(PUB_TOPIC_BUTTON, j_but.dump());
			pubmsg->set_qos(QOS);
			if (printoutSend)
			{
				printf("measured button status:  %d\n", pushbutton);
			}
			client.publish(pubmsg);// ->wait_for(TIMEOUT);
			sleep_for(milliseconds(8));
			if (printoutSend)
			{
				std::cout << "  ...OK" << std::endl;
			}
		}

	}
	while (false)
	{
		printf("Position: %f, %f, %f, Forces:  %f, %f, %f\n", px, py, pz, fx, fy, fz);
		//
	}
	printf("exiting application\n");

	dhdClose();

	// Disconnect

	try {
		std::cout << "\nDisconnecting from the MQTT server..." << std::flush;
		client.disconnect()->wait();
		std::cout << "OK" << std::endl;
	}
	catch (const mqtt::exception& exc) {
		std::cerr << exc.what() << std::endl;
		return 1;
	}

	return 0;
}
