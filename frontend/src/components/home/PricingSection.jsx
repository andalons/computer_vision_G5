import React from 'react';

const PricingSection = () => {
  const pricingPlans = [
    {
      name: 'Starter',
      price: '€299',
      period: '/month',
      description: 'Perfect for small agencies',
      features: [
        '50 video analyses/month',
        'Basic reporting',
        'Email support',
        '2 supported brands'
      ],
      cta: 'Start Free Trial',
      popular: false
    },
    {
      name: 'Professional',
      price: '€799',
      period: '/month',
      description: 'For growing marketing teams',
      features: [
        '200 video analyses/month',
        'Advanced analytics',
        'Priority support',
        'Custom branding',
        'API access'
      ],
      cta: 'Start Professional',
      popular: true
    },
    {
      name: 'Enterprise',
      price: 'Custom',
      period: '',
      description: 'For large agencies & brands',
      features: [
        'Unlimited analyses',
        'White-label solution',
        'Dedicated support',
        'Custom integrations',
        'Training & onboarding'
      ],
      cta: 'Contact Sales',
      popular: false
    }
  ];

  return (
    <section className="py-20 bg-humo-600">
      <div className="px-6 mx-auto max-w-7xl lg:px-8">
        <div className="mb-16 text-center">
          <h2 className="mb-6 text-4xl font-bold font-montserrat text-petroleo-500">
            Choose Your Plan
          </h2>
          <p className="max-w-2xl mx-auto text-xl font-source text-petroleo-300">
            Scale your logo detection capabilities with plans designed for agencies of every size
          </p>
        </div>

        <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
          {pricingPlans.map((plan, index) => (
            <div key={index} className={`flex flex-col bg-white rounded-card p-8 shadow-medium relative h-full ${plan.popular ? 'ring-2 ring-coral-500' : ''}`}>
              {plan.popular && (
                <div className="absolute transform -translate-x-1/2 -top-4 left-1/2">
                  <span className="px-4 py-1 text-sm font-medium text-white rounded-full bg-coral-500 font-montserrat">
                    Most Popular
                  </span>
                </div>
              )}
              
              <div className="mb-8 text-center">
                <h3 className="mb-2 text-2xl font-bold font-montserrat text-petroleo-500">
                  {plan.name}
                </h3>
                <p className="mb-4 font-source text-petroleo-300">
                  {plan.description}
                </p>
                <div className="flex items-baseline justify-center">
                  <span className="text-4xl font-bold font-montserrat text-petroleo-500">
                    {plan.price}
                  </span>
                  <span className="ml-1 font-source text-petroleo-300">
                    {plan.period}
                  </span>
                </div>
              </div>

              <ul className="flex-grow mb-8 space-y-4">
                {plan.features.map((feature, featureIndex) => (
                  <li key={featureIndex} className="flex items-center">
                    <div className="flex-shrink-0 w-2 h-2 mr-3 rounded-full bg-mostaza-500"></div>
                    <span className="font-source text-petroleo-400">{feature}</span>
                  </li>
                ))}
              </ul>

              <button className={`mt-auto w-full font-montserrat font-semibold text-base px-6 py-3 rounded-button transition-all duration-300 ${
                plan.popular 
                  ? 'bg-coral-500 text-white hover:bg-coral-400' 
                  : 'border-2 border-petroleo-300 text-petroleo-500 hover:border-coral-500 hover:text-coral-500'
              }`}>
                {plan.cta}
              </button>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default PricingSection;