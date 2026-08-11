module YakuDigitalTwin

using DifferentialEquations

export simulate_chlorine_decay

function simulate_chlorine_decay(C0::Float64, k::Float64,
                                 duration_s::Float64, dt_s::Float64)
    function f!(du, u, p, t)
        du[1] = -p[1] * u[1]
    end
    prob = ODEProblem(f!, [C0], (0.0, duration_s), [k])
    sol = solve(prob, Tsit5(), saveat=dt_s)
    return (
        time_s = collect(sol.t),
        chlorine_mg_l = [u[1] for u in sol.u],
    )
end

end
