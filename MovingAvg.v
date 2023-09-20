`timescale 1ns / 1ns
module MovingAvg
    #(  parameter DW = 18, 
		parameter log2_samples = 8,
		parameter US = 0)
    (
		//inputs
        input clk,
		input ENA,
        input rst_n,
        input signed [DW - 1 : 0] sample,
		//outputs
        output wire [DW - 1:0] avg
	);

    
// state registers
reg ENA_old;
reg signed [DW+log2_samples : 0] sum;
reg signed [DW+log2_samples : 0] r_avg;

wire [DW+log2_samples : 0] sample_signed_extended;

assign sample_signed_extended = ((US==0)? 	{ {(log2_samples+1){sample[DW-1]}}, sample[DW-1:0] } : { {(log2_samples){1'b0}}, sample[DW-1:0] });

//assign sample_signed_extended = { {(log2_samples){sample[DW-1]}}, sample[DW-1:0] };

assign avg = r_avg[DW-1:0];

// update our state variables
always @(posedge clk, negedge rst_n) begin
	if (!rst_n) begin
		r_avg <= 0;
		ENA_old <= 0;
        sum <= 0;
	end 
	else begin
		
		if(ENA_old==0 && ENA==1) begin
            sum <= sum + sample_signed_extended - r_avg;
		end
		if(US == 0)
			r_avg <= sum >>> log2_samples;
		else
			r_avg <= sum >> log2_samples;
			
		ENA_old <= ENA;
	end
end     
endmodule

